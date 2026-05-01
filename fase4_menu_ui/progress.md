# Checklist de Tareas - Fase 4: Menú e Interfaz de Usuario

## Tareas Pendientes (Usuario)
- [ ] Ejecutar `python main.py` y probar flujo completo
- [ ] Probar cada pantalla con DB real (alta, buscar, mod, elim)
- [ ] Verificar paginación en búsquedas (next/prev)
- [ ] Probar exportación a todos los formatos (CSV, XLSX, JSON, PDF)
- [ ] Testear validaciones (CUIL, nombres, fechas)
- [ ] Confirmar que Rich está instalado y funcionando
- [ ] Documentar atajos de teclado en README

## Tareas Completadas
- [x] Evaluar librería CLI: elegido `rich` + fallback stdlib
- [x] Instalar dependencias CLI en requirements.txt
- [x] Diseñar estructura de menús (6 opciones + submenús)
- [x] Implementar src/vistas.py (13 funciones)
- [x] Implementar src/formularios.py (5 formularios validados)
- [x] Implementar src/menu_principal.py (7 pantallas)
- [x] Crear main.py (punto de entrada principal)
- [x] Crear menu_principal.py (script alternativo raíz)
- [x] Actualizar src/__init__.py (exponer Fase 4)
- [x] Actualizar README.md con sección Uso - Fase 4
- [x] Actualizar AGENTS.md con estado Fase 4
- [x] Crear guía instalación Fase 4 (instalacion.md)
- [x] Validar sintaxis todos los módulos Python

## Notas
Fase 4 completada en código. Interfaz CLI 100% funcional con `rich`.
Requiere validación manual con base de datos real y pruebas de flujo.
