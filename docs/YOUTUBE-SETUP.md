# Автозагрузка на YouTube — настройка OAuth (делаешь ты, один раз, ~15 минут)

Загрузка идёт через YouTube Data API v3 (`videos.insert`) скриптом `scripts/youtube_upload.py`.
Пароли и токены вводишь только ты. В репозиторий токен не попадает: `.env` в `.gitignore`.

## 1. Проект в Google Cloud
1. Открой https://console.cloud.google.com/ под Google-аккаунтом, которому принадлежит канал **zylo**.
2. Сверху: выбор проекта → **New Project** → имя `zylo-uploader` → Create.
3. **APIs & Services → Library** → найди **YouTube Data API v3** → **Enable**.

## 2. Экран согласия (OAuth consent screen)
1. **APIs & Services → OAuth consent screen** (в новом интерфейсе — **Google Auth Platform → Branding/Audience**).
2. User type: **External** → Create. Имя приложения: `zylo uploader`, e-mail поддержки и разработчика — твой.
3. Scopes можно не добавлять вручную (скрипт сам их запросит).
4. **Audience → Test users** → добавь свой Gmail (владельца канала).
5. **Важно:** после первой успешной авторизации нажми **Publish app** (статус *In production*).
   В режиме *Testing* refresh-токен умирает через 7 дней, и автозагрузка сломается.
   Верификация Google для личного использования не нужна — при входе просто будет предупреждение
   «Google hasn't verified this app» → *Advanced* → *Go to zylo uploader (unsafe)*. Это твоё же приложение.

## 3. OAuth-клиент
1. **APIs & Services → Credentials → Create credentials → OAuth client ID**.
2. Application type: **Desktop app**, имя `zylo-desktop` → Create.
3. **Download JSON** → получишь `client_secret_XXXX.json`. Не публикуй и не присылай его в чат.

## 4. Получить refresh-токен (на своём компьютере)
```bash
pip install google-auth-oauthlib
```
```bash
python scripts/youtube_auth.py --client-secrets ~/Downloads/client_secret_XXXX.json
```
Откроется браузер → выбери аккаунт канала zylo (если аккаунт брендовый — выбери именно канал) → разреши доступ.
Скрипт напечатает три строки:
```
YT_CLIENT_ID=...
YT_CLIENT_SECRET=...
YT_REFRESH_TOKEN=...
```

## 5. Куда положить
- **Локально:** вставь три строки в файл `.env` в корне репозитория (он в `.gitignore`).
- **Для облачного/GitHub-запуска:** добавь их как секреты окружения:
  - облачная среда Claude Code: настройки окружения → Environment variables;
  - GitHub Actions: Settings → Secrets and variables → Actions → New repository secret (три секрета с теми же именами).

## 6. Проверка
```bash
.venv/bin/python scripts/youtube_upload.py --check
```
Должно вывести `"channel": "UCfoc78YxRz1DXNroyI688mA", "expected": true`.
Скрипт откажется загружать, если токен принадлежит другому каналу.

## Ограничения, о которых стоит знать
- Квота по умолчанию — 10 000 единиц/сутки; одна загрузка ≈ 1 600 → до ~6 видео в день. Нам нужно 1–2.
- Своя обложка (`thumbnails.set`) работает только на канале с подтверждённым номером телефона
  (YouTube Studio → Settings → Channel → Feature eligibility).
- Google пишет, что у непроверенных (unaudited) API-проектов загрузки могут принудительно становиться *private*.
  На практике это касается загрузок в чужие каналы; для своего канала обычно всё публикуется.
  Скрипт показывает реальный статус после загрузки; если увидим `private` — подадим проект на аудит
  (форма YouTube API Services Audit), это бесплатно.
