"""
Carga datos de PRUEBA (ficticios) para demostrar el sistema.

Uso:  python manage.py cargar_datos_prueba [--limpiar]

Las categorías se basan en las del Festival documentadas en la Entrega 1. Los nombres de
las opciones son genéricos ("Participante de prueba N"): no representan personas reales.
"""
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from festival.models import Categoria, Edicion, Opcion, Votacion

CATEGORIAS = [
    ("Acordeonero profesional", "Concurso central del Festival de música tradicional."),
    ("Canción vallenata inédita", "Composiciones originales que compiten en el Festival."),
    ("Piquería mayor", "Duelo de versos improvisados entre verseadores."),
    ("Conjuntos típicos", "Agrupaciones tradicionales de acordeón, caja y guacharaca."),
]


class Command(BaseCommand):
    help = "Carga ediciones, categorías, votaciones y opciones de prueba."

    def add_arguments(self, parser):
        parser.add_argument("--limpiar", action="store_true", help="Borra los datos del festival antes de cargar.")

    @transaction.atomic
    def handle(self, *args, **opts):
        if opts["limpiar"]:
            Edicion.objects.all().delete()
            self.stdout.write("Datos anteriores eliminados.")

        ahora = timezone.now()
        edicion27, _ = Edicion.objects.get_or_create(
            anio=2027,
            defaults=dict(
                nombre="Festival de la Leyenda Vallenata",
                descripcion="Edición 60 (datos de prueba para la Entrega 2).",
                fecha_inicio=date(2027, 4, 28),
                fecha_fin=date(2027, 5, 1),
                activa=True,
            ),
        )
        edicion26, _ = Edicion.objects.get_or_create(
            anio=2026,
            defaults=dict(
                nombre="Festival de la Leyenda Vallenata",
                descripcion="Edición 59 (histórica, datos de prueba).",
                fecha_inicio=date(2026, 4, 29),
                fecha_fin=date(2026, 5, 2),
                activa=True,
            ),
        )

        # (edición, índice de categoría, estado, apertura, cierre): cubre todos los estados.
        plan = [
            (edicion27, 0, Votacion.Estado.ABIERTA, ahora - timedelta(days=1), ahora + timedelta(days=5)),
            (edicion27, 1, Votacion.Estado.ABIERTA, ahora - timedelta(days=2), ahora + timedelta(days=3)),
            # «abierta» con apertura futura: el público la ve como «Próximamente».
            (edicion27, 2, Votacion.Estado.ABIERTA, ahora + timedelta(days=10), ahora + timedelta(days=15)),
            (edicion27, 3, Votacion.Estado.BORRADOR, ahora + timedelta(days=10), ahora + timedelta(days=15)),
            (edicion26, 0, Votacion.Estado.PUBLICADA, ahora - timedelta(days=400), ahora - timedelta(days=390)),
            (edicion26, 2, Votacion.Estado.CERRADA, ahora - timedelta(days=400), ahora - timedelta(days=395)),
        ]
        for edicion, idx, estado, apertura, cierre in plan:
            nombre, desc = CATEGORIAS[idx]
            cat, _ = Categoria.objects.get_or_create(
                edicion=edicion, nombre=nombre, defaults=dict(descripcion=desc, orden=idx + 1)
            )
            vot, creada = Votacion.objects.get_or_create(
                categoria=cat,
                nombre=f"Votación del público · {nombre} {edicion.anio}",
                defaults=dict(
                    descripcion="Votación de prueba. Elige a tu favorito entre los participantes.",
                    fecha_apertura=apertura,
                    fecha_cierre=cierre,
                    estado=estado,
                ),
            )
            if creada:
                for i in range(1, 5):
                    Opcion.objects.create(
                        votacion=vot,
                        nombre=f"Participante de prueba {i}",
                        descripcion="Dato de prueba, no corresponde a una persona real.",
                        orden=i,
                    )
        # Una categoría sin votaciones, para mostrar el estado vacío en la interfaz.
        Categoria.objects.get_or_create(
            edicion=edicion27, nombre="Acordeonera menor", defaults=dict(descripcion="Categoría juvenil.", orden=5)
        )
        self.stdout.write(self.style.SUCCESS(
            f"Listo: {Edicion.objects.count()} ediciones, {Categoria.objects.count()} categorías, "
            f"{Votacion.objects.count()} votaciones, {Opcion.objects.count()} opciones."
        ))
