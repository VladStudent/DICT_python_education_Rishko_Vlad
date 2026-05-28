import argparse
import math
import sys


def print_error_and_exit():
    """Виводить повідомлення про помилку та зупиняє програму."""
    print("Incorrect parameters")
    sys.exit(0)


def calculate_diff_payments(principal, periods, interest):
    """Розрахунок диференційованих платежів (Етап 4)."""
    i = interest / (12 * 100)

    total_paid = 0
    for m in range(1, periods + 1):
        dm = (principal / periods) + i * (principal - (principal * (m - 1)) / periods)
        dm_rounded = math.ceil(dm)
        total_paid += dm_rounded
        print(f"Month {m}: payment is {dm_rounded}")

    overpayment = total_paid - principal
    print(f"Overpayment = {overpayment}")


def calculate_annuity(principal, payment, periods, interest):
    """Розрахунок ануїтетних параметрів (Етап 3 та 4)."""
    i = interest / (12 * 100)

    if periods is None:
        log_base = 1 + i
        arg = payment / (payment - i * principal)
        n = math.ceil(math.log(arg, log_base))

        years = n // 12
        months = n % 12

        if years == 0:
            output_str = f"{months} months"
        elif months == 0:
            if years == 1:
                output_str = f"{years} year"
            else:
                output_str = f"{years} years"
        else:
            output_str = f"{years} years and {months} months"

        print(f"It will take {output_str} to repay this loan!")
        overpayment = (payment * n) - principal
        print(f"Overpayment = {overpayment}")

    elif payment is None:
        pow_part = math.pow(1 + i, periods)
        annuity = principal * ((i * pow_part) / (pow_part - 1))
        annuity_rounded = math.ceil(annuity)

        print(f"Your annuity payment = {annuity_rounded}!")
        overpayment = (annuity_rounded * periods) - principal
        print(f"Overpayment = {overpayment}")

    elif principal is None:
        pow_part = math.pow(1 + i, periods)
        p = payment / ((i * pow_part) / (pow_part - 1))
        p_rounded = math.floor(p)

        print(f"Your loan principal = {p_rounded}!")
        overpayment = (payment * periods) - p_rounded
        print(f"Overpayment = {overpayment}")


def main():
    parser = argparse.ArgumentParser(description="Credit Calculator")

    parser.add_argument("--type", choices=["annuity", "diff"], help="Type of payment")
    parser.add_argument("--principal", type=float, help="Loan principal")
    parser.add_argument("--payment", type=float, help="Monthly payment")
    parser.add_argument("--periods", type=int, help="Number of months")
    parser.add_argument("--interest", type=float, help="Loan interest")

    args = parser.parse_args()

    all_args = [args.type, args.principal, args.payment, args.periods, args.interest]
    provided_args_count = sum(1 for x in all_args if x is not None)

    if provided_args_count < 4:
        print_error_and_exit()

    if not args.type:
        print_error_and_exit()

    if args.interest is None:
        print_error_and_exit()

    for val in [args.principal, args.payment, args.periods, args.interest]:
        if val is not None and val < 0:
            print_error_and_exit()

    if args.type == "diff":
        if args.payment is not None:
            print_error_and_exit()
        calculate_diff_payments(
            int(args.principal), args.periods, args.interest
        )

    elif args.type == "annuity":
        principal_val = int(args.principal) if args.principal else None
        payment_val = int(args.payment) if args.payment else None

        calculate_annuity(principal_val, payment_val, args.periods, args.interest)


if __name__ == "__main__":
    main()