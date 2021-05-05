dictionary = {
    "LT": {
        "init_duration_ms": {
            "default": "Inicijavimo laikas (ms)",
            "genitive_case": "inicijavimo laiko (ms)"
        },
        "image_size_mb": {
            "default": "Atvaizdo dydis (MB)",
            "genitive_case": "atvaizdo dydžio (MB)"
        },
        "memory_size_mb": {
            "default": "Atmintis (MB)",
            "genitive_case": "atminties (MB)"
        },
        "vcpu_for_memory": {
            "default": 'Skiriama vCPU/s laiko (s)'
        },
        "chart_title": {
            "default": "Funkcijos inicijavimo laiko priklausomybė nuo {}"
        },
        "init_duration_ms_mean": {
            "default": "Inicijavimo laiko vidurkis (ms)",
        },
        "init_duration_ms_std": {
            "default": "Inicijavimo laiko standartinis nuokrypis (ms)",
        },
        "available_cpus": {
            "default": "Procesoriaus loginės gijos"
        }
    }
}


def translate(term, *args, language="LT"):
    try:
        language_translations = dictionary[language]
        translated_term = language_translations[term]["default"]
        return translated_term.format(*args)
    except KeyError:
        return 'Not_Defined_Term'


def genitive_case(term, language="LT"):
    try:
        language_translations = dictionary[language]
        return language_translations[term]["genitive_case"]
    except KeyError:
        return 'Not_Defined_Term'
