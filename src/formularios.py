"""
Módulo de formularios y validaciones de entrada - Fase 4.
"""

import re
from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator, ValidationError
from src.vistas import mostrar_mensaje

class CuilValidator(Validator):
    """Validador para formato CUIL: XX-XXXXXXXX-X"""
    def validate(self, document):
        text = document.text
        if not re.match(r'^\d{2}-\d{8}-\d{1}$', text):
            raise ValidationError(
                message='Formato inválido. Debe ser XX-XXXXXXXX-X',
                cursor_position=len(text)
            )

class RequiredValidator(Validator):
    """Validador para campos obligatorios."""
    def validate(self, document):
        if not document.text.strip():
            raise ValidationError(
                message='Este campo es obligatorio',
                cursor_position=len(document.text)
            )

def solicitar_datos_persona(default_data: dict = None) -> dict:
    """Solicita los datos de una persona mediante prompts validados."""
    print("\nIngrese los datos solicitados (Ctrl+C para cancelar):")
    
    try:
        nombre = prompt(
            'Nombre: ', 
            default=default_data.get('nombre', '') if default_data else '',
            validator=RequiredValidator()
        ).strip()
        
        apellido = prompt(
            'Apellido: ', 
            default=default_data.get('apellido', '') if default_data else '',
            validator=RequiredValidator()
        ).strip()
        
        cuil = prompt(
            'CUIL (XX-XXXXXXXX-X): ', 
            default=default_data.get('cuil', '') if default_data else '',
            validator=CuilValidator()
        ).strip()
        
        return {
            'nombre': nombre,
            'apellido': apellido,
            'cuil': cuil
        }
    except KeyboardInterrupt:
        return None

def confirmar_accion(mensaje: str) -> bool:
    """Solicita una confirmación S/N."""
    resultado = prompt(f"{mensaje} (s/N): ").lower().strip()
    return resultado == 's'
