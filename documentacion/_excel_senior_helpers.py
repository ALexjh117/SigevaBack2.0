# -*- coding: utf-8 -*-
def ca(cid, tipo, dado, cuando, entonces):
    return {"id": cid, "tipo": tipo, "dado": dado, "cuando": cuando, "entonces": entonces}


def cp(cid, cubre, escenario, esperado, tipo="Feliz"):
    return {"id": cid, "cubre": cubre, "escenario": escenario, "esperado": esperado, "tipo": tipo}
