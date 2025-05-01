from classes.glpi_adapter import Glpi
import os

def main():
    glpi = Glpi()
    tickets = glpi.get_ticket()
    tecnicos = glpi.get_users()
    
    if not tickets:
        print("Nenhum chamado disponível.")
        return
    
    if not tecnicos:
        print("Nenhum técnico disponível.")
        return

    #Ordena os técnicos
    tecnicos_ordenados = glpi.score_chamados(tecnicos)

    for ticket in tickets:
        tecnico_selecionado = tecnicos_ordenados[0]  #Tecnico menos sobrecarregado
        glpi.distribui_chamado(ticket, tecnico_selecionado)

        #Atualiza a contagem de chamados do tecnico selecionado
        tecnico_selecionado["ticket_count"] += 1

        #Reordena a lista de tecnicos
        tecnicos_ordenados = glpi.score_chamados(tecnicos)

if __name__ == '__main__':
    main()