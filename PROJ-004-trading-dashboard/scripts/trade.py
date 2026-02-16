#!/usr/bin/env python3
"""
CLI Script /trade - Registro Rápido de Trades
PROJ-004 Trading Dashboard

Usage:
    python trade.py --interactive
    python trade.py --json '{"datetime": "2024-01-15T14:30:00", "profile": "trend_alta", "result_percent": 2.5, "result_usdt": 125.0, "leverage": 10, "setup": "scalp_1m", "entry": 43250.50, "tp": 43500.00, "sl": 43000.00}'
    python trade.py --file trades.json
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Optional
import requests

# Configuração da API (variáveis de ambiente)
API_BASE_URL = "http://localhost:3000/api"
API_TOKEN = "your-api-token-here"

# Perfis válidos
VALID_PROFILES = [
    "grid",
    "trend_alta",
    "trend_baixa",
    "lateralizacao",
    "breakout"
]

# Setups comuns
VALID_SETUPS = [
    "scalp_1m",
    "scalp_5m",
    "scalp_15m",
    "daytrade_1h",
    "daytrade_4h",
    "swing_1d",
    "swing_1w",
    "custom"
]


def validate_datetime(dt_str: str) -> tuple[bool, str]:
    """Valida formato de data/hora."""
    try:
        datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return True, ""
    except ValueError:
        return False, f"Data/hora inválida: {dt_str}. Use formato ISO: YYYY-MM-DDTHH:MM:SS"


def validate_profile(profile: str) -> tuple[bool, str]:
    """Valida o perfil do trade."""
    if profile not in VALID_PROFILES:
        return False, f"Perfil inválido: {profile}. Valores válidos: {', '.join(VALID_PROFILES)}"
    return True, ""


def validate_result(result_percent: float, result_usdt: float) -> tuple[bool, str]:
    """Valida os resultados do trade."""
    if not isinstance(result_percent, (int, float)):
        return False, "result_percent deve ser um número"
    if not isinstance(result_usdt, (int, float)):
        return False, "result_usdt deve ser um número"
    return True, ""


def validate_prices(entry: float, tp: float, sl: float) -> tuple[bool, str]:
    """Valida preços de entrada, TP e SL."""
    for price in [entry, tp, sl]:
        if not isinstance(price, (int, float)) or price <= 0:
            return False, "Preços devem ser números positivos"
    
    if not (tp > entry or sl < entry):
        return False, "TP deve ser maior que entrada e SL menor que entrada (para trades long)"
    return True, ""


def validate_leverage(leverage: int) -> tuple[bool, str]:
    """Valida alavancagem."""
    if not isinstance(leverage, int) or leverage < 1 or leverage > 125:
        return False, "Alavancagem deve ser um inteiro entre 1 e 125"
    return True, ""


def validate_setup(setup: str) -> tuple[bool, str]:
    """Valida o setup utilizado."""
    if setup not in VALID_SETUPS:
        return False, f"Setup inválido: {setup}. Valores válidos: {', '.join(VALID_SETUPS)}"
    return True, ""


def validate_trade_data(data: dict) -> tuple[bool, list[str]]:
    """
    Valida todos os dados do trade.
    Returns: (is_valid, list_of_errors)
    """
    errors = []
    
    required_fields = {
        'datetime': ('string', validate_datetime),
        'profile': ('string', validate_profile),
        'result_percent': ('number', None),
        'result_usdt': ('number', None),
        'leverage': ('number', validate_leverage),
        'setup': ('string', validate_setup),
        'entry': ('number', None),
        'tp': ('number', None),
        'sl': ('number', None)
    }
    
    # Check required fields
    for field, (expected_type, validator) in required_fields.items():
        if field not in data:
            errors.append(f"Campo obrigatório ausente: {field}")
            continue
        
        value = data[field]
        
        if expected_type == 'string' and not isinstance(value, str):
            errors.append(f"Campo {field} deve ser string")
        elif expected_type == 'number' and not isinstance(value, (int, float)):
            errors.append(f"Campo {field} deve ser número")
        
        if validator and isinstance(value, (str, int, float)):
            valid, error_msg = validator(value)
            if not valid:
                errors.append(error_msg)
    
    # Validate prices relationship
    if all(k in data for k in ['entry', 'tp', 'sl']):
        valid, error = validate_prices(data['entry'], data['tp'], data['sl'])
        if not valid:
            errors.append(error)
    
    return len(errors) == 0, errors


def send_to_api(data: dict) -> tuple[bool, dict]:
    """Envia dados do trade para a API."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/trades",
            json=data,
            headers={"Authorization": f"Bearer {API_TOKEN}"},
            timeout=10
        )
        
        if response.status_code == 201:
            return True, response.json()
        else:
            return False, {"error": f"API Error: {response.status_code}", "details": response.text}
    
    except requests.exceptions.RequestException as e:
        return False, {"error": str(e)}


def save_locally(data: dict, filename: str = "trades_local.json") -> tuple[bool, str]:
    """Salva trade localmente como backup."""
    try:
        # Read existing file
        try:
            with open(filename, 'r') as f:
                trades = json.load(f)
        except FileNotFoundError:
            trades = []
        
        # Add new trade
        data['saved_at'] = datetime.now().isoformat()
        trades.append(data)
        
        # Write back
        with open(filename, 'w') as f:
            json.dump(trades, f, indent=2)
        
        return True, f"Salvo em {filename}"
    
    except Exception as e:
        return False, f"Erro ao salvar localmente: {str(e)}"


def interactive_mode() -> dict:
    """Modo interativo via CLI."""
    print("\n=== Registro de Trade ===\n")
    
    data = {}
    
    # Datetime
    default_dt = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    data['datetime'] = input(f"Data/Hora [{default_dt}]: ").strip() or default_dt
    
    # Profile
    print(f"\nPerfis válidos: {', '.join(VALID_PROFILES)}")
    data['profile'] = input("Perfil: ").strip().lower()
    
    # Results
    data['result_percent'] = float(input("Resultado (%): ").strip())
    data['result_usdt'] = float(input("Resultado (USDT): ").strip())
    
    # Leverage
    data['leverage'] = int(input("Alavancagem (1-125): ").strip())
    
    # Setup
    print(f"\nSetups válidos: {', '.join(VALID_SETUPS)}")
    data['setup'] = input("Setup: ").strip().lower()
    
    # Prices
    data['entry'] = float(input("Entrada: ").strip())
    data['tp'] = float(input("Take Profit (TP): ").strip())
    data['sl'] = float(input("Stop Loss (SL): ").strip())
    
    # Optional notes
    data['notes'] = input("\nNotas (opcional): ").strip()
    
    return data


def main():
    parser = argparse.ArgumentParser(
        description="CLI para registro rápido de trades - PROJ-004 Trading Dashboard"
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Modo interativo"
    )
    parser.add_argument(
        "--json", "-j",
        type=str,
        help="Dados do trade em formato JSON"
    )
    parser.add_argument(
        "--file", "-f",
        type=str,
        help="Arquivo JSON contendo lista de trades"
    )
    parser.add_argument(
        "--save-only",
        action="store_true",
        help="Salva apenas localmente (não envia para API)"
    )
    parser.add_argument(
        "--api-url",
        type=str,
        help="URL base da API (sobrescreve padrão)"
    )
    
    args = parser.parse_args()
    
    if not any([args.interactive, args.json, args.file]):
        parser.print_help()
        print("\nExemplos:")
        print("  python trade.py --interactive")
        print("  python trade.py --json '{\"datetime\": \"2024-01-15T14:30:00\", ...}'")
        print("  python trade.py --file trades.json")
        sys.exit(1)
    
    # Collect trade data
    if args.interactive:
        trade_data = interactive_mode()
    elif args.json:
        try:
            trade_data = json.loads(args.json)
        except json.JSONDecodeError as e:
            print(f"Erro ao parsear JSON: {e}")
            sys.exit(1)
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                all_trades = json.load(f)
                if not isinstance(all_trades, list):
                    print("Arquivo deve conter lista de trades")
                    sys.exit(1)
                trade_data = all_trades[0]  # Process first trade
        except Exception as e:
            print(f"Erro ao ler arquivo: {e}")
            sys.exit(1)
    
    # Validate data
    print("\n=== Validação ===")
    is_valid, errors = validate_trade_data(trade_data)
    
    if not is_valid:
        print("❌ Erros de validação:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    
    print("✅ Dados válidos!")
    
    # Show summary
    print("\n=== Resumo do Trade ===")
    print(f"Data/Hora: {trade_data['datetime']}")
    print(f"Perfil: {trade_data['profile']}")
    print(f"Resultado: {trade_data['result_percent']}% ({trade_data['result_usdt']} USDT)")
    print(f"Alavancagem: {trade_data['leverage']}x")
    print(f"Setup: {trade_data['setup']}")
    print(f"Entrada: {trade_data['entry']} | TP: {trade_data['tp']} | SL: {trade_data['sl']}")
    
    # Send to API or save locally
    if not args.save_only:
        print("\n=== Enviando para API ===")
        if args.api_url:
            global API_BASE_URL
            API_BASE_URL = args.api_url
        
        success, response = send_to_api(trade_data)
        
        if success:
            print("✅ Trade registrado com sucesso na API!")
            print(f"ID: {response.get('id', 'N/A')}")
        else:
            print(f"⚠️ Erro na API: {response.get('error')}")
            print("Salvando localmente como backup...")
            success, msg = save_locally(trade_data)
            if success:
                print(f"✅ {msg}")
            else:
                print(f"❌ {msg}")
                sys.exit(1)
    else:
        success, msg = save_locally(trade_data)
        if success:
            print(f"\n✅ {msg}")
        else:
            print(f"\n❌ {msg}")
            sys.exit(1)


if __name__ == "__main__":
    main()
