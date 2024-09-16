# django-zanwango
A Django based web framework, combining the best of DRF and Django Ninja

# Main goals of the project:

- Modernize DRF
- Use pydantic instead of serializers (Initially use Django Ninja)
- Fully typed
- Full async support
- Full support OpenAPI
- As compatible as possible with DRF and its batteries. Use of protocols.
- Allow composition over inheritance in viewset methods
- Some batteries included, but not limited to:
  - filtering
  - sorting (with aliases too)
  - field selector & viewset config
  - snake2camel renderer

# Installation

Install using `pip`...

    pip install django-zanwango

Add `"zanwango"` to your `INSTALLED_APPS` setting.
```python
INSTALLED_APPS = [
    ...
    "zanwango",
]
```