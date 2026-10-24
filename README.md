# Captcha Solver

Скрипт для автоматического прохождения Cloudflare Interstitial капчи с использованием Playwright.

## Требования

- Python 3.10+
- Google Chrome (установленный в системе)

## Установка

```bash
uv sync
```

Установить браузер для patchright:

```bash
patchright install chromium
```

## Настройка

Создай файл `.env` в корне проекта:

```env
VFS_URL=https://example.com/page
HEADLESS=False
MAX_RETRIES=3
```

| Переменная    | Описание                                      | По умолчанию |
|---------------|-----------------------------------------------|--------------|
| `VFS_URL`     | URL страницы с капчей                         | —            |
| `HEADLESS`    | Запуск без окна браузера (`True` / `False`)   | `False`      |
| `MAX_RETRIES` | Количество попыток решения                    | `3`          |

## Запуск

```bash
python captcha_solver.py
```

Скрипт откроет браузер, перейдёт по указанному URL и попытается пройти капчу. В случае неудачи повторит попытку (с паузой между попытками).