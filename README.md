# Магазин рыбы в телеграм

Данный проект позволяет с помощью `бота` покупать покупать рыбу в `телеграме`.


## Что необходимо для запуска
Для данного проекта необходим `Python3.10` (или выше).

Создадим виртуальное окружение в корневой директории проекта:
```sh
python3 -m venv env
```
Активируйте его. На разных операционных системах это делается разными командами:

- Windows: `.\venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`

Установим необходимые зависимости:
```sh
pip install -r requirements.txt
```



# 🚀 Getting started with Strapi

Strapi comes with a full featured [Command Line Interface](https://docs.strapi.io/dev-docs/cli) (CLI) which lets you scaffold and manage your project in seconds.

### `develop`

Start your Strapi application with autoReload enabled. [Learn more](https://docs.strapi.io/dev-docs/cli#strapi-develop)

```
npm run develop
# or
yarn develop
```

### `start`

Start your Strapi application with autoReload disabled. [Learn more](https://docs.strapi.io/dev-docs/cli#strapi-start)

```
npm run start
# or
yarn start
```

### `build`

Build your admin panel. [Learn more](https://docs.strapi.io/dev-docs/cli#strapi-build)

```
npm run build
# or
yarn build
```

## ⚙️ Deployment

Strapi gives you many possible deployment options for your project including [Strapi Cloud](https://cloud.strapi.io). Browse the [deployment section of the documentation](https://docs.strapi.io/dev-docs/deployment) to find the best solution for your use case.

## 📚 Learn more

- [Resource center](https://strapi.io/resource-center) - Strapi resource center.
- [Strapi documentation](https://docs.strapi.io) - Official Strapi documentation.
- [Strapi tutorials](https://strapi.io/tutorials) - List of tutorials made by the core team and the community.
- [Strapi blog](https://strapi.io/blog) - Official Strapi blog containing articles made by the Strapi team and the community.
- [Changelog](https://strapi.io/changelog) - Find out about the Strapi product updates, new features and general improvements.

Feel free to check out the [Strapi GitHub repository](https://github.com/strapi/strapi). Your feedback and contributions are welcome!

## ✨ Community

- [Discord](https://discord.strapi.io) - Come chat with the Strapi community including the core team.
- [Forum](https://forum.strapi.io/) - Place to discuss, ask questions and find answers, show your Strapi project and get feedback or just talk with other Community members.
- [Awesome Strapi](https://github.com/strapi/awesome-strapi) - A curated list of awesome things related to Strapi.

---
##### Разверните локальную CMS и наполните ее данными.
<sub>🤫 Psst! [Strapi is hiring](https://strapi.io/careers).</sub>




Для телеграм бота потребуются настройки переменных окружения из файла `.env`:
```sh
TGTOKEN = 'токен вашего бота в телеграм'

TELEGRAM_ADMIN_ID = 'ID вашего администратора в телеграм'

BASE_URL = 'http://localhost:1337'

```

Для редактирования подключения `redis` : необходимо создать файл `.env`


```sh
REDIS_HOST = 'host'

REDIS_PORT = 'port'

REDIS_PASSWORD = 'password'
```


## Запуск бота
Бот запускается командой
```
python tg_bot.py
```

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
