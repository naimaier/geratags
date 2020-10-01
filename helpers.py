def generate(data, model_number):
    generator = _get_generator(model_number)
    return generator(data)


def _get_generator(model_number):
    if model_number == 1:
        return _generate_model_1
    elif model_number == 2:
        return _generate_model_2
    elif model_number == 3:
        return _generate_model_3
    else:
        raise ValueError(model_number)


def _get_symbol(data):
    return data["name"].replace("-", "")


def _generate_model_1(data):
    symbol = _get_symbol(data)

    # Modelo AG
    output_file_data = {
        "#ID": data["id"],
        "#Name": '"' + data["name"] + '"',
        "#bitManAuto": "int_" + symbol + "[0]",
        "#bitLigaMan": "int_" + symbol + "[1]",
        "#bitStsLigadoMan": "int_" + symbol + "[2]",
        "#bitStsLigadoAuto": "int_" + symbol + "[3]",
        "#bitStsFalha": "int_" + symbol + "[4]",
        "#bitResetHorimetro": "int_" + symbol + "[5]",
        "#bitLocalRemoto": "int_" + symbol + "[6]",
        "#intHorimetro": "int_hor_" + symbol
    }
    return output_file_data


def _generate_model_2(data):
    symbol = _get_symbol(data)

    # Modelo BP
    output_file_data = {
        "#ID": data["id"],
        "#Name": '"' + data["name"] + '"',
        "#bitManAuto": "int_" + symbol + "[0]",
        "#bitLigaMan": "int_" + symbol + "[1]",
        "#bitStsLigadoMan": "int_" + symbol + "[2]",
        "#bitStsLigadoAuto": "int_" + symbol + "[3]",
        "#bitStsFalha": "int_" + symbol + "[4]",
        "#bitResetHorimetro": "int_" + symbol + "[5]",
        "#bitLocalRemoto": "int_" + symbol + "[6]",
        "#intHorimetro": "int_hor_" + symbol,
        "#intCtrVel": "int_setpoint_man_" + symbol,
        "#intStsVel": "int_sts_ve_" + symbol,
        "#intStsCurr": "int_sts_curr_" + symbol,
        "#intFalha": "int_sts_falha_" + symbol
    }

    return output_file_data


def _generate_model_3(data):
    symbol = _get_symbol(data)

    # Modelo TT
    output_file_data = {
        "#ID": data["id"],
        "#Name": '"' + data["name"] + '"',
        "#intSts": "int_sts_" + symbol.lower(),
        "#realSns": "real_" + symbol.lower(),
        "#realMinSns": "real_" + symbol.lower() + "_min",
        "#realMaxSns": "real_" + symbol.lower() + "_max",
    }

    return output_file_data