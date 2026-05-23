from backend.storage import agenda_repo


def consultar_agenda(periodo: str) -> str:
    if periodo == "hoje":
        events = agenda_repo.get_today()
        label = "hoje"
    elif periodo == "amanha":
        events = agenda_repo.get_tomorrow()
        label = "amanhã"
    else:
        events = agenda_repo.get_week()
        label = "nos próximos 7 dias"

    if not events:
        return f"Nenhum evento encontrado para {label}."

    lines = [f"Eventos {label}:"]
    for e in events:
        time_str = f" às {e['time']}" if e.get("time") else ""
        loc_str = f" — {e['location']}" if e.get("location") else ""
        lines.append(f"  [{e['date']}{time_str}] {e['title']}{loc_str} ({e['type']})")
    return "\n".join(lines)
