# 🏥 MenVitta Backend

Bienvenido al backend del sistema **MenVitta**, una plataforma enfocada en la gestión médica de citas y pacientes.

## 🚀 Tech Stack

- Django
- Django REST Framework
- PostgreSQL
- Docker
- GitHub Actions (próximamente)

## 📦 Cómo levantar el proyecto en local

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/menvitta-backend.git
   cd menvitta-backend
   ```

2. Crea un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   ```

3. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Copia el archivo de entorno:
   ```bash
   cp .env.example .env
   ```

5. Corre migraciones:
   ```bash
   python manage.py migrate
   ```

6. Corre el servidor:
   ```bash
   python manage.py runserver
   ```

## 📄 License

Este proyecto está licenciado bajo la Licencia MIT.