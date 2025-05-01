
# 🤝 Guía de Contribución / Contributing Guide

¡Gracias por tu interés en contribuir a este proyecto!  
Thanks for your interest in contributing to this project!

---

## 📋 Reglas generales / General Rules

- Sé respetuoso y profesional en todas las interacciones.
- Antes de abrir un issue o PR, revisa si ya existe uno similar.
- Sigue el flujo de trabajo y el estilo de código del proyecto.
- Si tienes dudas, pregunta en los canales de contacto.

---

## 🚀 ¿Cómo contribuir? / How to contribute?

1. **Forkea** este repositorio y crea una rama desde `main` o la rama relevante.
2. Haz tus cambios siguiendo las [buenas prácticas](#-estilo-de-código--code-style).
3. Asegúrate de que los tests pasen y el código esté formateado.
4. Abre un Pull Request explicando claramente tus cambios.
5. Espera feedback y haz los ajustes necesarios.

---

## 🐞 Reportar bugs / Reporting bugs

- Usa el [formulario de bug](../../issues/new?template=bug_report.yml) para reportar errores.
- Incluye pasos claros para reproducir el problema, entorno y evidencia visual si es posible.

---

## 🚀 Sugerir features / Suggesting features

- Usa el [formulario de feature](../../issues/new?template=feature_request.yml) para proponer nuevas funcionalidades.
- Explica el objetivo y el beneficio para el proyecto.

---

## 📝 Mejorar documentación / Improving documentation

- Usa el [formulario de documentación](../../issues/new?template=docs_issue.yml) para sugerir cambios o mejoras en la documentación.

---

## 🧑‍💻 Estilo de código / Code style (Python, Django, DRF, JWT)

**Español:**
- Sigue la [PEP8](https://peps.python.org/pep-0008/) para Python.
- Usa nombres descriptivos y en inglés para variables, funciones y clases.
- Organiza los imports siguiendo el orden: estándar, terceros, locales (usa [isort](https://pycqa.github.io/isort/)).
- Usa [black](https://black.readthedocs.io/en/stable/) para formatear el código automáticamente.
- Usa [flake8](https://flake8.pycqa.org/en/latest/) para linting y detectar errores comunes.
- Para Django:
  - Usa convenciones de nombres para modelos (`CamelCase`), vistas (`CamelCase` para clases, `snake_case` para funciones).
  - Mantén las vistas delgadas y la lógica en los serializers o managers.
  - Usa señales solo cuando sea necesario.
- Para Django REST Framework (DRF):
  - Prefiere `ViewSets` y `Routers` para APIs RESTful.
  - Usa serializers para validación y transformación de datos.
  - Documenta los endpoints y usa [drf-yasg](https://drf-yasg.readthedocs.io/en/stable/) o [drf-spectacular](https://drf-spectacular.readthedocs.io/) para documentación automática.
- Para JWT:
  - Nunca expongas claves secretas en el código.
  - Usa librerías seguras como [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/).
  - Valida y protege los endpoints sensibles con permisos adecuados.
- Escribe comentarios claros y docstrings en clases, métodos y funciones.
- Mantén el código modular y reutilizable.
- No dejes código muerto ni prints de debug en los commits finales.

**English:**
- Follow [PEP8](https://peps.python.org/pep-0008/) for Python code style.
- Use descriptive, English names for variables, functions, and classes.
- Organize imports in the order: standard, third-party, local (use [isort](https://pycqa.github.io/isort/)).
- Use [black](https://black.readthedocs.io/en/stable/) for automatic code formatting.
- Use [flake8](https://flake8.pycqa.org/en/latest/) for linting and catching common errors.
- For Django:
  - Use naming conventions: `CamelCase` for models and class-based views, `snake_case` for functions.
  - Keep views thin; put business logic in serializers or managers.
  - Use signals only when necessary.
- For Django REST Framework (DRF):
  - Prefer `ViewSets` and `Routers` for RESTful APIs.
  - Use serializers for validation and data transformation.
  - Document endpoints and use [drf-yasg](https://drf-yasg.readthedocs.io/en/stable/) or [drf-spectacular](https://drf-spectacular.readthedocs.io/) for automatic API docs.
- For JWT:
  - Never expose secret keys in code.
  - Use secure libraries like [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/).
  - Validate and protect sensitive endpoints with proper permissions.
- Write clear comments and docstrings for classes, methods, and functions.
- Keep code modular and reusable.
- Do not leave dead code or debug prints in final commits.

---

## 🧪 Tests

- Agrega o actualiza tests para cubrir tus cambios.
- Asegúrate de que todos los tests pasen antes de abrir un PR.

---

## 📦 Commits y Pull Requests

- Escribe mensajes de commit claros y descriptivos.
- Relaciona tu PR con el issue correspondiente usando `Closes #número`.
- Llena el template de Pull Request y sigue el checklist.

---

## 📞 Contacto / Contact

- 📧 Email: [humberto.morales.14@hotmail.com](mailto:humberto.morales.14@hotmail.com)
- 💼 LinkedIn: [bert0h-dev](https://www.linkedin.com/in/bert0h-dev/)

---

## 🙏 ¡Gracias por contribuir! / Thank you for contributing!

Tu ayuda hace que este proyecto sea mejor para todos.  
Your help makes this project better for everyone.

---
