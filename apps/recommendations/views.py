"""
Views for crop recommendations.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Recommendation
from .forms import RecommendationRequestForm, MagicRecommendationForm
from .services import CropRecommendationService
from apps.farms.models import Farm, Field
from apps.soil.models import SoilData
from apps.weather.models import WeatherData
from apps.weather.services import WeatherDataService
from apps.soil.services import SoilDataService

@login_required
def recommendation_request(request):
    """Request crop recommendations via Magic Flow or for an existing field."""
    form = RecommendationRequestForm(user=request.user)
    magic_form = MagicRecommendationForm()
    
    if request.method == 'POST':
        # Check which form was submitted by checking a hidden field or distinguishing inputs
        if 'farm_name' in request.POST:
            # Magic Flow Processing
            magic_form = MagicRecommendationForm(request.POST)
            if magic_form.is_valid():
                lat = magic_form.cleaned_data['latitude']
                lon = magic_form.cleaned_data['longitude']
                farm_name = magic_form.cleaned_data['farm_name']
                area = magic_form.cleaned_data['area']
                
                # 1. Auto-create Farm
                farm, created = Farm.objects.get_or_create(
                    user=request.user,
                    name=farm_name,
                    defaults={'latitude': lat, 'longitude': lon, 'area': area}
                )
                
                # 2. Auto-create Main Field
                field, f_created = Field.objects.get_or_create(
                    farm=farm,
                    name=f"{farm_name} - Main Field",
                    defaults={'latitude': lat, 'longitude': lon, 'area': area}
                )
                
                # 3. Auto-fetch Weather
                weather_data_dict = WeatherDataService.get_weather_data(lat, lon)
                weather_data = None
                if weather_data_dict:
                    weather_data, _ = WeatherData.objects.update_or_create(
                        latitude=lat, longitude=lon, date=timezone.now().date(),
                        defaults={
                            'temperature': weather_data_dict.get('temperature', 25),
                            'rainfall': weather_data_dict.get('rainfall', 0),
                            'humidity': weather_data_dict.get('humidity', 50),
                            'wind_speed': weather_data_dict.get('wind_speed', 0),
                        }
                    )
                
                # 4. Auto-fetch Soil
                soil_data_dict = SoilDataService.get_soil_data(lat, lon, source='auto')
                if soil_data_dict:
                    SoilData.objects.create(
                        field=field,
                        ph=soil_data_dict.get('ph'),
                        moisture=soil_data_dict.get('moisture'),
                        n=soil_data_dict.get('n'),
                        p=soil_data_dict.get('p'),
                        k=soil_data_dict.get('k'),
                        source=soil_data_dict.get('source', 'auto')
                    )
                    # Update field fields
                    field.soil_ph = soil_data_dict.get('ph')
                    field.soil_moisture = soil_data_dict.get('moisture')
                    field.n_content = soil_data_dict.get('n')
                    field.p_content = soil_data_dict.get('p')
                    field.k_content = soil_data_dict.get('k')
                    field.save()
                
                # 5. Get Recommendations
                recommendations = CropRecommendationService.get_recommendation_for_field(
                    field=field, weather_data=weather_data, limit=10
                )
                
                if not recommendations:
                    messages.warning(request, 'No recommendations available based on current data.')
                    return render(request, 'recommendations/recommendation_request.html', 
                                 {'form': form, 'magic_form': magic_form})
                
                # Save recommendations
                saved_recommendations = []
                for rec in recommendations[:5]:
                    reasoning_data = {
                        'reasons': rec['reasons'],
                        'match_details': rec['match_details']
                    }
                    if 'profit_details' in rec: reasoning_data['profit_details'] = rec['profit_details']
                    if 'sustainability_details' in rec: reasoning_data['sustainability_details'] = rec['sustainability_details']
                    if 'rotation_analysis' in rec: reasoning_data['rotation_analysis'] = rec['rotation_analysis']
                    
                    recommendation = Recommendation.objects.create(
                        user=request.user,
                        field=field,
                        crop_name=rec['crop_name'],
                        confidence_score=rec['confidence_score'],
                        expected_yield=rec['expected_yield'],
                        profit_margin=rec['profit_margin'],
                        sustainability_score=rec['sustainability_score'],
                        reasoning=reasoning_data
                    )
                    saved_recommendations.append(recommendation)
                
                messages.success(request, f'Magic Flow generated {len(recommendations)} recommendations for {field.name}!')
                context = {
                    'field': field,
                    'recommendations': recommendations,
                    'saved_recommendations': saved_recommendations,
                    'weather_data': weather_data,
                }
                return render(request, 'recommendations/recommendation_results.html', context)
        
        else:
            # Old standard flow
            form = RecommendationRequestForm(request.POST, user=request.user)
            if form.is_valid():
                farm = form.cleaned_data['farm']
                include_weather = form.cleaned_data.get('include_weather', True)
                
                # Get or create the main field for this farm
                field = farm.fields.first()
                if not field:
                    field = Field.objects.create(
                        farm=farm,
                        name=f"{farm.name} - Main Field",
                        latitude=farm.latitude,
                        longitude=farm.longitude,
                        area=farm.area
                    )
                
                # Auto-fetch Weather
                lat, lon = float(field.latitude or farm.latitude), float(field.longitude or farm.longitude)
                weather_data = None
                if include_weather:
                    weather_dict = WeatherDataService.get_weather_data(lat, lon)
                    if weather_dict:
                        weather_data, _ = WeatherData.objects.update_or_create(
                            latitude=lat, longitude=lon, date=timezone.now().date(),
                            defaults={
                                'temperature': weather_dict.get('temperature', 25),
                                'rainfall': weather_dict.get('rainfall', 0),
                                'humidity': weather_dict.get('humidity', 50),
                                'wind_speed': weather_dict.get('wind_speed', 0),
                            }
                        )
                
                # Auto-fetch Soil if missing
                if not field.soil_ph or not field.n_content:
                    soil_dict = SoilDataService.get_soil_data(lat, lon, source='auto')
                    if soil_dict:
                        SoilData.objects.create(
                            field=field, ph=soil_dict.get('ph'), moisture=soil_dict.get('moisture'),
                            n=soil_dict.get('n'), p=soil_dict.get('p'), k=soil_dict.get('k'), source='auto'
                        )
                        field.soil_ph = soil_dict.get('ph')
                        field.soil_moisture = soil_dict.get('moisture')
                        field.n_content = soil_dict.get('n')
                        field.p_content = soil_dict.get('p')
                        field.k_content = soil_dict.get('k')
                        field.save()
                
                recommendations = CropRecommendationService.get_recommendation_for_field(
                    field=field,
                    weather_data=weather_data,
                    limit=10
                )
                
                if not recommendations:
                    messages.warning(request, 'No recommendations available based on current data.')
                    return render(request, 'recommendations/recommendation_request.html', {'form': form, 'magic_form': magic_form})
                
                saved_recommendations = []
                for rec in recommendations[:5]:
                    existing = Recommendation.objects.filter(user=request.user, field=field, crop_name=rec['crop_name']).order_by('-created_at').first()
                    reasoning_data = {'reasons': rec['reasons'], 'match_details': rec['match_details']}
                    if 'profit_details' in rec: reasoning_data['profit_details'] = rec['profit_details']
                    if 'sustainability_details' in rec: reasoning_data['sustainability_details'] = rec['sustainability_details']
                    if 'rotation_analysis' in rec: reasoning_data['rotation_analysis'] = rec['rotation_analysis']
                    
                    if existing:
                        existing.confidence_score = rec['confidence_score']
                        existing.expected_yield = rec['expected_yield']
                        existing.profit_margin = rec['profit_margin']
                        existing.sustainability_score = rec['sustainability_score']
                        existing.reasoning = reasoning_data
                        existing.save()
                        saved_recommendations.append(existing)
                    else:
                        recommendation = Recommendation.objects.create(
                            user=request.user, field=field, crop_name=rec['crop_name'],
                            confidence_score=rec['confidence_score'], expected_yield=rec['expected_yield'],
                            profit_margin=rec['profit_margin'], sustainability_score=rec['sustainability_score'],
                            reasoning=reasoning_data
                        )
                        saved_recommendations.append(recommendation)
                
                messages.success(request, f'Generated {len(recommendations)} crop recommendations for {field.name}!')
                context = {
                    'field': field, 'recommendations': recommendations,
                    'saved_recommendations': saved_recommendations, 'weather_data': weather_data,
                }
                return render(request, 'recommendations/recommendation_results.html', context)
    
    return render(request, 'recommendations/recommendation_request.html', {'form': form, 'magic_form': magic_form})


@login_required
def recommendation_list(request):
    """List all recommendations for the current user."""
    recommendations = Recommendation.objects.filter(
        user=request.user
    ).select_related('field', 'field__farm').order_by('-created_at')[:50]
    
    context = {
        'recommendations': recommendations,
    }
    return render(request, 'recommendations/recommendation_list.html', context)


@login_required
def recommendation_detail(request, pk):
    """View recommendation details."""
    recommendation = get_object_or_404(
        Recommendation,
        pk=pk,
        user=request.user
    )
    
    context = {
        'recommendation': recommendation,
    }
    return render(request, 'recommendations/recommendation_detail.html', context)


@login_required
def recommendation_for_field(request, field_pk):
    """Get recommendations for a specific field."""
    field = get_object_or_404(Field, pk=field_pk, farm__user=request.user)
    
    # Get latest weather data
    weather_data = None
    if field.latitude and field.longitude:
        weather_data = WeatherData.objects.filter(
            latitude=field.latitude,
            longitude=field.longitude
        ).order_by('-date').first()
    elif field.farm.latitude and field.farm.longitude:
        weather_data = WeatherData.objects.filter(
            latitude=field.farm.latitude,
            longitude=field.farm.longitude
        ).order_by('-date').first()
    
    # Get recommendations
    recommendations = CropRecommendationService.get_recommendation_for_field(
        field=field,
        weather_data=weather_data,
        limit=10
    )
    
    context = {
        'field': field,
        'recommendations': recommendations,
        'weather_data': weather_data,
    }
    return render(request, 'recommendations/recommendation_results.html', context)
