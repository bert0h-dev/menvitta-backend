
# 🏥 MenVitta Backend

<div align="center" markdown="1">

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-4.x-green.svg)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-14%2B-blue.svg)](https://www.postgresql.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

</div>

---

## 🇪🇸 Español | 🇬🇧 English

<details>
<summary><strong>Español</strong></summary>

## 📚 Documentación oficial

Toda la documentación técnica y de usuario está centralizada en:

👉 [https://github.com/bert0h-dev/menvitta-docs](https://github.com/bert0h-dev/menvitta-docs)

Consulta ahí la guía de la API, modelos, ejemplos, y más.


## 📋 Tabla de Contenido

- [Descripción](#descripción)
- [Tech Stack](#tech-stack)
- [Demo](#demo)
- [Instalación](#instalación)
- [Comandos útiles](#comandos-útiles)
- [Contribución](#contribución)
- [Seguridad](#seguridad)
- [Comunidad y contacto](#comunidad-y-contacto)
- [Licencia](#licencia)

## 📄 Descripción

**MenVitta Backend** es la API REST para la plataforma MenVitta, enfocada en la gestión médica de citas y pacientes.  
Incluye autenticación JWT, manejo de usuarios, zonas horarias, internacionalización y más.

## 🛠️ Tech Stack

- **Python 3.10+**
- **Django 4.x**
- **Django REST Framework**
- **PostgreSQL**
- **Docker**
- **JWT (djangorestframework-simplejwt)**
- **GitHub Actions** (CI/CD)
- **Dependabot** (seguridad de dependencias)

## 🚀 Demo

> _Próximamente: ejemplos de endpoints y respuestas_

## 💻 Instalación

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

## 🛠️ Comandos útiles

- Ejecutar tests:
  ```bash
  python manage.py test
  ```
- Crear superusuario:
  ```bash
  python manage.py createsuperuser
  ```
- Levantar con Docker (opcional):
  ```bash
  docker-compose up --build
  ```

## 🤝 Contribución

¡Las contribuciones son bienvenidas!  
Lee la [Guía de Contribución](CONTRIBUTING.md) antes de abrir un PR o issue.

- [Abrir un Issue](../../issues/new/choose)
- [Abrir un Pull Request](../../compare)

## 🛡️ Seguridad

¿Encontraste una vulnerabilidad?  
Por favor revisa nuestra [Política de Seguridad](SECURITY.md) y repórtala de forma privada.

## 🌐 Comunidad y contacto

- 💼 [LinkedIn](https://www.linkedin.com/in/bert0h-dev/)
- 📧 [Email](mailto:humberto.morales.14@hotmail.com)

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT.

</details>

---

<details>
<summary><strong>English</strong></summary>

## 📚 Official Documentation

All technical and user documentation is now centralized at:

👉 [https://github.com/bert0h-dev/menvitta-docs](https://github.com/bert0h-dev/menvitta-docs)

Please refer to that repository for the API guide, models, examples, and more.

## 📋 Table of Contents

- [Description](#description)
- [Tech Stack](#tech-stack-1)
- [Demo](#demo-1)
- [Installation](#installation)
- [Useful Commands](#useful-commands)
- [Contributing](#contributing)
- [Security](#security)
- [Community & Contact](#community--contact)
- [License](#license)

## 📄 Description

**MenVitta Backend** is the REST API for the MenVitta platform, focused on medical appointment and patient management.  
Includes JWT authentication, user management, timezone support, internationalization, and more.

## 🛠️ Tech Stack

- **Python 3.10+**
- **Django 4.x**
- **Django REST Framework**
- **PostgreSQL**
- **Docker**
- **JWT (djangorestframework-simplejwt)**
- **GitHub Actions** (CI/CD)
- **Dependabot** (dependency security)

## 🚀 Demo

> _Coming soon: endpoint and response examples_

## 💻 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-user/menvitta-backend.git
   cd menvitta-backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy the environment file:
   ```bash
   cp .env.example .env
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Run the server:
   ```bash
   python manage.py runserver
   ```

## 🛠️ Useful Commands

- Run tests:
  ```bash
  python manage.py test
  ```
- Create superuser:
  ```bash
  python manage.py createsuperuser
  ```
- Run with Docker (optional):
  ```bash
  docker-compose up --build
  ```

## 🤝 Contributing

Contributions are welcome!  
Read the [Contributing Guide](CONTRIBUTING.md) before opening a PR or issue.

- [Open an Issue](../../issues/new/choose)
- [Open a Pull Request](../../compare)

## 🛡️ Security

Found a vulnerability?  
Please review our [Security Policy](SECURITY.md) and report it privately.

## 🌐 Community & Contact

- 💼 [LinkedIn](https://www.linkedin.com/in/bert0h-dev/)
- 📧 [Email](mailto:humberto.morales.14@hotmail.com)

## 📄 License

This project is licensed under the MIT License.

</details>
