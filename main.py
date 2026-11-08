# main.py
# Gestor de conteúdos textuais - FASE 2
# Já funcionam: carregar textos, listar, pesquisar, ver corpo e tamanho.
# Palavras proibidas, sentimento e relatório ficam para a fase seguinte.

import os

LARGURA = 46  # largura da "moldura" do ecrã
PASTA_BASE = os.path.dirname(os.path.abspath(__file__))
PASTA_TEXTOS = os.path.join(PASTA_BASE, "textos")
# Se não existir a pasta "textos", usa a pasta do próprio main.py
# (assim funciona também com os .txt soltos ao lado do main.py).
if not os.path.isdir(PASTA_TEXTOS):
    PASTA_TEXTOS = PASTA_BASE


# ---------------------------------------------------------------
# Carregamento dos textos
# ---------------------------------------------------------------
def carregar_textos(pasta):
    """Lê todos os .txt da pasta. A 1.ª linha é o título, o resto é o corpo.
    Devolve uma lista de dicionários com id, ficheiro, titulo, corpo, tamanho."""
    textos = []
    if not os.path.isdir(pasta):
        return textos

    ficheiros = sorted(f for f in os.listdir(pasta) if f.lower().endswith(".txt"))
    for numero, nome in enumerate(ficheiros, start=1):
        try:
            with open(os.path.join(pasta, nome), "r", encoding="utf-8") as f:
                linhas = f.read().splitlines()
        except (OSError, UnicodeDecodeError):
            print("  [!] Não foi possível ler o ficheiro:", nome)
            continue

        titulo = linhas[0].strip() if linhas else "(sem título)"
        corpo = "\n".join(linhas[1:]).strip()
        textos.append({
            "id": numero,
            "ficheiro": nome,
            "titulo": titulo,
            "corpo": corpo,
            "tamanho": len(corpo),
        })
    return textos


def procurar_por_id(textos, id_texto):
    """Devolve o texto com esse ID, ou None se não existir."""
    for texto in textos:
        if texto["id"] == id_texto:
            return texto
    return None


# ---------------------------------------------------------------
# Funções de apresentação
# ---------------------------------------------------------------
def mostrar_cabecalho(subtitulo=""):
    """Desenha o cabeçalho do programa (e um subtítulo opcional)."""
    print()
    print("╔" + "═" * (LARGURA - 2) + "╗")
    print("║" + "GESTOR DE CONTEÚDOS TEXTUAIS".center(LARGURA - 2) + "║")
    if subtitulo != "":
        print("║" + subtitulo.center(LARGURA - 2) + "║")
    print("╚" + "═" * (LARGURA - 2) + "╝")


def mostrar_menu_inicial():
    """Mostra as opções do menu principal."""
    mostrar_cabecalho()
    print(" 1) Listar textos")
    print(" 2) Pesquisar textos por palavra-chave")
    print(" 3) Processar texto")
    print(" 4) Listar palavras proibidas")
    print(" 5) Adicionar palavra proibida")
    print(" 6) Apagar palavra proibida")
    print(" 0) Sair")


def mostrar_menu_processamento(id_texto):
    """Mostra o submenu de processamento de um texto."""
    mostrar_cabecalho("Processamento de texto")
    print(" Texto selecionado -> ID", id_texto)
    print()
    print(" 1) Visualizar corpo")
    print(" 2) Ver tamanho do corpo")
    print(" 3) Listar palavras proibidas no texto")
    print(" 4) Realizar análise de sentimento")
    print(" 5) Criar relatório completo")
    print(" 6) Voltar ao menu inicial")


def mostrar_lista(textos):
    """Mostra textos no formato: ID | ficheiro | título."""
    print("\n ID | Ficheiro | Título")
    print(" " + "-" * (LARGURA - 2))
    for t in textos:
        print(f" {t['id']} | {t['ficheiro']} | {t['titulo']}")


# ---------------------------------------------------------------
# Funções de leitura de input (com validação)
# ---------------------------------------------------------------
def ler_opcao(opcoes_validas):
    """Pede uma opção até o utilizador escrever uma que seja válida."""
    while True:
        escolha = input("\nEscolha uma opção: ").strip()
        if escolha in opcoes_validas:
            return escolha
        print("  [!] Opção inválida. Tente uma destas:", ", ".join(opcoes_validas))


def ler_id(textos):
    """Pede o ID de um texto até ser um inteiro que exista."""
    while True:
        try:
            valor = int(input("\nIndique o ID do texto: "))
        except ValueError:
            print("  [!] Tem de escrever um número inteiro.")
            continue
        if procurar_por_id(textos, valor) is not None:
            return valor
        print("  [!] Não existe nenhum texto com o ID", valor)


def esperar_enter():
    """Pausa para o utilizador ler a mensagem antes de voltar ao menu."""
    input("\n(prima ENTER para continuar)")


# ---------------------------------------------------------------
# Funcionalidades
# ---------------------------------------------------------------
def listar_textos(textos):
    mostrar_lista(textos)


def pesquisar_textos(textos, palavra):
    """Procura a palavra (sem distinguir maiúsculas) no título e no corpo."""
    if palavra == "":
        print("\n  [!] Não escreveu nenhuma palavra-chave.")
        return
    chave = palavra.lower()
    encontrados = [t for t in textos
                   if chave in t["titulo"].lower() or chave in t["corpo"].lower()]
    if not encontrados:
        print(f"\n  Nenhum texto contém '{palavra}'.")
    else:
        print(f"\n  {len(encontrados)} texto(s) com '{palavra}':")
        mostrar_lista(encontrados)


def visualizar_corpo(texto):
    print("\n--- " + texto["titulo"] + " ---")
    print(texto["corpo"] if texto["corpo"] else "(corpo vazio)")


def ver_tamanho(texto):
    palavras = len(texto["corpo"].split())
    print(f"\n  Tamanho do corpo: {texto['tamanho']} caracteres ({palavras} palavras)")


# ---------------------------------------------------------------
# Submenu "Processar texto"
# ---------------------------------------------------------------
def menu_processar_texto(textos):
    id_texto = ler_id(textos)
    texto = procurar_por_id(textos, id_texto)

    while True:
        mostrar_menu_processamento(id_texto)
        escolha = ler_opcao(["1", "2", "3", "4", "5", "6"])

        if escolha == "1":
            visualizar_corpo(texto)
        elif escolha == "2":
            ver_tamanho(texto)
        elif escolha == "3":
            print("\n>> [em desenvolvimento] Palavras proibidas no texto", id_texto)
        elif escolha == "4":
            print("\n>> [em desenvolvimento] Análise de sentimento do texto", id_texto)
        elif escolha == "5":
            print("\n>> [em desenvolvimento] Relatório do texto", id_texto)
        else:  # "6"
            return

        esperar_enter()


# ---------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------
def main():
    textos = carregar_textos(PASTA_TEXTOS)
    if not textos:
        print("Não foram encontrados ficheiros .txt na pasta:", PASTA_TEXTOS)
        print("Adicione textos a essa pasta e volte a executar o programa.")
        return

    print(f"{len(textos)} texto(s) carregado(s).")

    while True:
        mostrar_menu_inicial()
        escolha = ler_opcao(["0", "1", "2", "3", "4", "5", "6"])

        if escolha == "1":
            listar_textos(textos)
        elif escolha == "2":
            palavra = input("\nPalavra-chave a pesquisar: ").strip()
            pesquisar_textos(textos, palavra)
        elif escolha == "3":
            menu_processar_texto(textos)
            continue  # o submenu já tratou das pausas
        elif escolha == "4":
            print("\n>> [em desenvolvimento] Listar palavras proibidas")
        elif escolha == "5":
            palavra = input("\nPalavra proibida a adicionar: ").strip()
            print("\n>> [em desenvolvimento] Adicionar:", palavra)
        elif escolha == "6":
            palavra = input("\nPalavra proibida a apagar: ").strip()
            print("\n>> [em desenvolvimento] Apagar:", palavra)
        else:  # "0"
            print("\nObrigado por usar o Gestor. Até à próxima!")
            break

        esperar_enter()


if __name__ == "__main__":
    main()
