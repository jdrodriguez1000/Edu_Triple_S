"""
Nivel 5 - Script 0: probar el detector ANTES de gastar plata.

LA IDEA:
    01_contar.py va a decidir, respuesta por respuesta, si hay rioplatense.
    Ese detector es codigo escrito por un humano y puede estar mal.
    Si el detector miente, el experimento entero miente -- con toda la
    apariencia de rigor, porque igual imprime un numero bonito.

    Asi que el detector se prueba primero, con textos que escribimos
    nosotros y cuya respuesta correcta ya conocemos.

POR QUE ESTE SCRIPT NO CUESTA NADA:
    No llama a la API ni una vez. Prueba solo TU codigo.
    Es la mitad determinista del nivel 5 (los evals de tipo 1), y es la
    parte que se puede correr mil veces sin factura.

    Se apoya en L4.14: la infraestructura SI es determinista aunque el
    modelo no lo sea. Aqui no hay modelo, asi que esto se comporta como
    cualquier programa normal: mismo input, mismo output, siempre.

USO:
    python 00_probar_detector.py
"""

import importlib.util
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# Cargamos 01_contar.py como modulo para reusar su detector.
# (Se hace asi porque el nombre empieza por numero y no se puede
# escribir 'import 01_contar'.)
def cargar(nombre, alias):
    ruta = Path(__file__).resolve().parent / nombre
    spec = importlib.util.spec_from_file_location(alias, ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


contar = cargar("01_contar.py", "contar")     # detector de dialecto
v2 = cargar("02_contar_v2.py", "contar_v2")   # detector de tratamiento


# ---------------------------------------------------------------------------
# LOS CASOS
# ---------------------------------------------------------------------------
# Estan puestos en PARES MINIMOS: dos frases que dicen lo mismo y se
# diferencian en una sola cosa. Es la mejor forma de probar un detector,
# porque si los dos miembros del par dan el mismo veredicto, el detector
# no esta mirando lo que crees que mira.
#
# (Misma tecnica del ejercicio 9 del nivel 4: para aislar un efecto,
#  cambias UNA cosa y dejas todo lo demas igual.)

CASOS = [
    # (texto, esperamos_rioplatense, por_que)
    ("Llevá campera y paraguas, que está lloviendo.", True,
     "voseo imperativo + lexico"),
    ("Lleva sombrilla y una chaqueta impermeable.", False,
     "PAR del anterior: solo cambia la tilde"),

    ("Si querés, ponete botas.", True,
     "voseo verbal + imperativo voseante"),
    ("Si quieres, ponte botas de caucho.", False,
     "PAR del anterior: forma colombiana"),

    ("Cuidate del aguacero, abrigate bien.", True,
     "imperativos voseantes sin tilde"),
    ("Cuídate del aguacero, abrígate bien.", False,
     "PAR del anterior: tuteo, con tilde en la i"),

    ("Ponte un saco y lleva sombrilla, usted sabe como es Bogota.", False,
     "colombiano puro: no debe dar ni un falso positivo"),
    ("Nosotros vamos ahora.", False,
     "trampa: 'vos' vive dentro de 'nosotros' -- lo salva el \\b"),
    ("Vos sos de Buenos Aires.", True,
     "voseo pronominal explicito"),
]


# ---------------------------------------------------------------------------
# LOS CASOS DEL SEGUNDO DETECTOR: tratamiento (tu / usted)
# ---------------------------------------------------------------------------
# Este detector nacio de MIRAR los datos, no de planearlo: al leer las 10
# respuestas de la v1 se vio que el modelo trataba de "tu" en 4 y de
# "usted" en 5, con el mismo prompt. Nadie fue a buscar eso.

CASOS_TRATO = [
    ("Ponte una chaqueta y llévate una sombrilla.", "tu",
     "imperativos con enclitico de tuteo"),
    ("Póngase una chaqueta y lleve una sombrilla.", "usted",
     "PAR del anterior: imperativos de usted"),

    ("Estas cosas pasan mucho en Bogotá.", "indeterminado",
     "TRAMPA: 'estas' sin tilde es demostrativo, no el verbo 'estás'"),
    ("Si estás en Bogotá, abrígate.", "tu",
     "PAR del anterior: 'estás' CON tilde si es tuteo"),

    ("Te recomiendo que lleve chaqueta impermeable.", "mixto",
     "se contradice dentro de la misma frase: 'te' + 'lleve'"),
    ("Hace frío y llueve en la ciudad.", "indeterminado",
     "no hay marcador: el detector debe poder decir 'no se'"),
    ("Usted puede llevar una sombrilla.", "usted",
     "pronombre explicito"),
]


def detectar(texto):
    """Exactamente lo que hace 01_contar.py. Si cambias uno, cambia el otro."""
    return (contar.buscar(texto, contar.MARCADORES_RIOPLATENSES)
            + contar.buscar(texto, contar.IMPERATIVOS_VOSEANTES,
                            quitar_tildes=False))


def main():
    print("=" * 74)
    print("  PROBANDO LOS DETECTORES (sin llamar a la API, costo $0.00)")
    print("=" * 74)

    # ---- detector 1: dialecto ------------------------------------------
    print("\n  [1/2] DETECTOR DE DIALECTO (rioplatense)\n")
    pasaron = 0
    for texto, esperado, porque in CASOS:
        hallados = detectar(texto)
        obtenido = len(hallados) > 0
        bien = obtenido == esperado

        pasaron += 1 if bien else 0
        sello = "  OK  " if bien else " FALLA"
        print(f"{sello}  esperado={str(esperado):<5}  obtuvo={str(obtenido):<5}")
        print(f"         \"{texto}\"")
        print(f"         ({porque})")
        if hallados:
            print(f"         marcadores: {', '.join(hallados)}")
        print()

    print(f"  --> {pasaron} de {len(CASOS)} casos de dialecto pasaron")

    # ---- detector 2: tratamiento ---------------------------------------
    print("\n" + "=" * 74)
    print("\n  [2/2] DETECTOR DE TRATAMIENTO (tu / usted)\n")
    pasaron_t = 0
    for texto, esperado, porque in CASOS_TRATO:
        obtenido, marcas_tu, marcas_ud = v2.tratamiento(texto)
        bien = obtenido == esperado

        pasaron_t += 1 if bien else 0
        sello = "  OK  " if bien else " FALLA"
        print(f"{sello}  esperado={esperado:<14} obtuvo={obtenido:<14}")
        print(f"         \"{texto}\"")
        print(f"         ({porque})")
        if marcas_tu or marcas_ud:
            print(f"         tu: {marcas_tu or '-'}   usted: {marcas_ud or '-'}")
        print()

    print(f"  --> {pasaron_t} de {len(CASOS_TRATO)} casos de trato pasaron")

    # ---- veredicto ------------------------------------------------------
    total = pasaron + pasaron_t
    esperados = len(CASOS) + len(CASOS_TRATO)
    print("\n" + "=" * 74)
    print(f"  {total} de {esperados} casos pasaron")
    print("=" * 74)

    if total != esperados:
        print("\n  NO corras 02_contar_v2.py todavia. Un detector esta mal y")
        print("  gastarias plata para obtener un numero que no significa nada.")
        sys.exit(1)

    print("\n  Detectores confiables dentro de lo que estos casos cubren.")
    print("  OJO con la letra pequeña: esto prueba que aciertan en los casos")
    print("  QUE SE ME OCURRIERON. Un marcador que no este en la lista sigue")
    print("  siendo invisible para el programa.")
    print("  Ese hueco es exactamente lo que el juez del tipo 2 viene a tapar.")


if __name__ == "__main__":
    main()
