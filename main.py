from vision.analyzer import analisar
from control.actions import executar

def main():
    resultado = analisar()
    executar(resultado)

if __name__ == "__main__":
    main()
