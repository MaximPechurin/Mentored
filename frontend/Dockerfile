FROM node:20-alpine

WORKDIR /app

# Копируем зависимости
COPY package*.json ./
RUN npm install

# Копируем код
COPY . .

# Собираем проект
RUN npm run build

# Устанавливаем простой сервер для отдачи статики
RUN npm install -g serve

EXPOSE 5173

CMD ["serve", "-s", "dist", "-l", "5173"]