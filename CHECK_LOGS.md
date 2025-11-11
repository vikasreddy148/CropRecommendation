# How to Check Django Server Logs

## Quick Guide

### 1. **Console/Terminal Logs (Most Common)**

When you run the Django development server with:
```bash
python manage.py runserver
```

All logs appear **directly in the terminal/console** where you ran the command. This includes:
- HTTP requests (GET, POST, etc.)
- Errors and exceptions
- Translation service logs
- Database queries (if DEBUG=True)

**Look for:**
- Translation errors: `Translation failed for text: ...`
- Google Translate errors: `Google Translate error: ...`
- Warnings: `googletrans not available...`

### 2. **Log File**

After adding the logging configuration, logs are also saved to:
```
logs/django.log
```

View the log file:
```bash
# View entire log file
cat logs/django.log

# View last 50 lines
tail -n 50 logs/django.log

# Follow log file in real-time (like tail -f)
tail -f logs/django.log
```

### 3. **Filter Translation Logs**

To see only translation-related logs:

```bash
# In terminal (while server is running)
# Look for lines containing "translation" or "translate"

# In log file
grep -i "translation" logs/django.log
grep -i "translate" logs/django.log
```

### 4. **Common Log Messages to Look For**

#### Translation Service Initialization:
- ✅ `Google Translate initialized and tested successfully`
- ⚠️ `googletrans not available. Install with: pip install googletrans==4.0.0rc1`
- ⚠️ `Failed to initialize Google Translate: ...`

#### Translation Operations:
- ✅ `Translation cache hit for: ...` (working, using cache)
- ⚠️ `Translation failed for text: '...' to language: hi`
- ⚠️ `Falling back to LibreTranslate for: ...`
- ⚠️ `Google Translate error: ...`

### 5. **Enable More Verbose Logging**

To see even more details, change the log level in `settings.py`:

```python
'apps.translation': {
    'handlers': ['console', 'file'],
    'level': 'DEBUG',  # Change from INFO to DEBUG for more details
    'propagate': False,
},
```

### 6. **Check Browser Console**

Also check your browser's developer console (F12) for:
- JavaScript errors
- Network errors (failed API calls)
- Console.log messages

### 7. **Test Translation Directly**

Run this in Django shell to test translation:
```bash
python manage.py shell
```

Then:
```python
from apps.translation.services import translate_text
result = translate_text("Hello", "hi")
print(f"Translation result: {result}")
```

### 8. **Common Issues and Log Messages**

| Issue | Log Message | Solution |
|-------|-------------|----------|
| googletrans not installed | `googletrans not available` | `pip install googletrans==4.0.0rc1` |
| Translation API error | `Google Translate error: ...` | Check internet connection, API limits |
| Translation failed | `Translation failed for text: ...` | Check language code, text format |
| Cache issue | No cache hit messages | Clear cache: `python manage.py clear_cache` |

### 9. **Real-time Monitoring**

While the server is running, keep the terminal visible. You'll see:
- Every HTTP request
- Translation attempts
- Errors immediately

### 10. **Production Logs**

In production, logs are typically:
- Written to files in `/var/log/` or similar
- Managed by systemd, supervisor, or similar
- Rotated automatically to prevent disk space issues

## Quick Commands Reference

```bash
# Start server and see logs
python manage.py runserver

# View log file
tail -f logs/django.log

# Filter translation logs
grep -i translation logs/django.log

# Clear Django cache (if translations are cached incorrectly)
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
```

## Next Steps

1. **Start your server** and watch the terminal
2. **Switch language** to Hindi in the UI
3. **Check terminal** for translation-related messages
4. **Look for errors** like "Translation failed" or "Google Translate error"
5. **Share the error messages** if translations aren't working

