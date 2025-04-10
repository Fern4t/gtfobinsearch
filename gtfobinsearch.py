#!/usr/bin/python3
import requests, time, signal, sys, argparse, os
from bs4 import BeautifulSoup
from pathlib import Path

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
tipos_permisos = {'all','shell','command','reverse-shell','non-interactive-reverse-shell','bind-shell','non-interactive-bind-shell','file-upload','file-download','file-write','file-read','library-load','suid','sudo','capabilities','limited-sudo'}


# Gestión de argumentos:

parser = argparse.ArgumentParser(
        description="Herramienta pra comprobar si se puede utilizar algún permiso para escalar privilegios"
)

parser.add_argument(
        '-b', '--bin', required=True,
        help='Nombre o path del binario a comprobar'
)

parser.add_argument(
        '-m', '--mode', default = 'all',
        help='Tipo de permiso. Ej: suid, sudo, capabilities...'
)

parser.add_argument(
        '-v','--verbose', action='store_true',
        help='Muestra los pasos a seguir para la escalada'
)

args = parser.parse_args()

# Comprueba si el binario existe en la web con el apartado permission. Si -v, muestra la descripcion y comandos
def main_search(binary, permission, verbose=False):

    if permission not in tipos_permisos:
        print(f'{RED}[!] Permission not allowed{RESET}')
        sys.exit(1)

    if permission == 'all': # Para mostrar todos los permisos de los binarios indicados
        all_mode(binary)
        sys.exit(0)

    ruta = Path(binary)

    if ruta.is_file(): # Comprueba si le estamos pasando una archivo o un binario (PELIGRO, SI INTRODUCIMOS LA RUTA DE UN BINARIO DEL SISTEMA, NO FUNCIONARÁ)
        file = open(binary, 'r')
        rutas = file.read().splitlines()
        for line in rutas:
            just_binary = os.path.basename(line)
            search_for_binary(just_binary,permission,verbose)
    else:
        search_for_binary(os.path.basename(binary),permission,verbose)

# Busca todos los permisos que se pueden explotar para el binario indicado.
def all_mode(binary):
    ruta = Path(binary)
    r1 = requests.get(url_principal)

    if ruta.is_file():
        file = open(binary, 'r')
        rutas = file.read().splitlines()
        for line in rutas:
            just_binary = os.path.basename(line)
            for perm in tipos_permisos:
                if (f"/gtfobins/{just_binary}/#{perm}") in r1.text:
                    print(f"\n{GREEN}[+]{RESET} El binario {GREEN}{just_binary}{RESET} puede aprovechar los permisos {GREEN}{perm}{RESET}")

    else:
        just_binary = os.path.basename(binary)
        for perm in tipos_permisos:
            if (f"/gtfobins/{just_binary}/#{perm}") in r1.text:
                print(f"\n{GREEN}[+]{RESET} El binario {GREEN}{just_binary}{RESET} puede aprovechar los permisos {GREEN}{perm}{RESET}")

# Busca si existe un binario con un permiso especifico
def search_for_binary(binary,permission,verbose):

    r1 = requests.get(url_principal)
    if (f"/gtfobins/{binary}/#{permission}") in r1.text:
        print(f"{GREEN}[+]{RESET} {GRAY}El binario{RESET} {GREEN}{binary}{RESET}{GRAY} con privilegio {GREEN}{permission}{RESET}{GRAY} es {GREEN}{GRAY}apto{RESET}")
        if verbose:
            time.sleep(0.5)
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

    main_search(args.bin, args.mode, args.verbose)

