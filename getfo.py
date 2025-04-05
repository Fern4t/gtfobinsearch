#!/usr/bin/python3
import requests, time, signal, sys, argparse
from bs4 import BeautifulSoup

# Basic color codes
GRAY="\033[1;37m"
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
RESET = '\033[0m'

def def_handler(sig, frame):

    print(f"\n\n{RED}[!] Ctrl + C detected. Cancelling the execution of the script... {RESET}\n")
    sys.exit(1)

# Ctrl + C
signal.signal(signal.SIGINT, def_handler)

# Variables globales
url_principal = 'https://gtfobins.github.io'

# Gestión de argumentos:

parser = argparse.ArgumentParser(
        description="Herramienta pra comprobar si se puede utilizar algún permiso para escalar privilegios"
)

parser.add_argument(
        '-b', '--bin', required=True,
        help='Nombre o path del binario a comprobar'
)

parser.add_argument(
        '-m', '--mode', required=True,
        help='Tipo de permiso. Ej: suid, sudo, capabilities...'
)

parser.add_argument(
        '-v','--verbose', action='store_true',
        help='Muestra los pasos a seguir para la escalada'
)

args = parser.parse_args()

# Comprueba si el binario existe en la web con el apartado permission. Si -v, muestra la descripcion y comandos (MEJORAR ENTRADA DE USUARIO EQUIPARANDO PATH A NOMBRE DEL BINARIO)
def search_for_binary(binary, permission, verbose):

    r1 = requests.get(url_principal)
    if (f"/gtfobins/{binary}/#{permission}") in r1.text:
        print(f"{GREEN}[+]{RESET} {GRAY}El binario{RESET} {GREEN}{binary}{RESET}{GRAY} con privilegio {GREEN}{permission}{RESET}{GRAY} es {GREEN}{GRAY}apto{RESET}")
        if verbose:
            time.sleep(1)
            search_for_instructions(binary, permission)
    else:
        print(f"{RED}[!]{RESET} {GRAY}El binario {RED}{binary}{RESET} {GRAY}con permiso {RED}{permission} NO{RESET}{GRAY} es apto{RESET}")

# Muestra la descripcion y los comandos necesarios para la escalada. (MEJORAR LA FORMA DE MOSTRAR LOS DATOS. ELIMINAR ETIQUETAS HTML Y ACLARAR LOS CODIGOS)
def search_for_instructions(binary, permission): 

            r2 = requests.get(url_principal + "/gtfobins/" + binary + "/#" + permission)
            html_content = r2.text
            soup = BeautifulSoup(html_content, 'html.parser') 
            permission_section = soup.find('h2', id=str(permission))
            print(f"\n{GREEN}[+]{GRAY} Descripción: {RESET}\n" + str(permission_section.find_next('p')))
            print(f"\n{GREEN}[+]{GRAY} Pasos a seguir: {RESET}\n" + str(permission_section.find_next('ul')))

if __name__ == '__main__':

    print(f"\n")
    search_for_binary(args.bin, args.mode, args.verbose)

