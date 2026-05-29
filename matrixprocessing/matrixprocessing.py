import sys

def read_matrix(prompt_size="Enter size of matrix: ", prompt_matrix="Enter matrix: "):
    """Зчитує розміри та матрицю з консолі, підтримує int та float."""
    try:
        size_input = input(prompt_size).strip().split()
        if not size_input:
            return None
        rows = int(size_input[0])
        cols = int(size_input[1])
    except (ValueError, IndexError):
        return None

    print(prompt_matrix)
    matrix = []
    for _ in range(rows):
        row = []
        line_elements = input().strip().split()
        for x in line_elements:
            if '.' in x:
                row.append(float(x))
            else:
                try:
                    row.append(int(x))
                except ValueError:
                    row.append(float(x))
        matrix.append(row)
    return matrix


def print_matrix(matrix):
    """Виводить матрицю у красивому форматі без відображення її розмірів."""
    for row in matrix:
        formatted_row = []
        for val in row:
            if isinstance(val, float):

                if abs(val) < 1e-9:
                    val = 0.0

                if val.is_integer():
                    formatted_row.append(str(val))
                else:
                    formatted_row.append(f"{round(val, 2)}")
            else:
                formatted_row.append(str(val))
        print(" ".join(formatted_row))



def add_matrices(matrix_a, matrix_b):
    """Етап 1: Додавання двох матриць."""
    if len(matrix_a) != len(matrix_b) or len(matrix_a[0]) != len(matrix_b[0]):
        return None

    result = []
    for i in range(len(matrix_a)):
        row = [matrix_a[i][j] + matrix_b[i][j] for j in range(len(matrix_a[0]))]
        result.append(row)
    return result


def multiply_by_constant(matrix, constant):
    """Етап 2: Множення матриці на константу."""
    result = []
    for row in matrix:
        result.append([item * constant for item in row])
    return result


def multiply_matrices(matrix_a, matrix_b):
    """Етап 3: Множення двох матриць."""
    if len(matrix_a[0]) != len(matrix_b):
        return None

    result = [[0] * len(matrix_b[0]) for _ in range(len(matrix_a))]
    for i in range(len(matrix_a)):
        for j in range(len(matrix_b[0])):
            total = 0
            for k in range(len(matrix_a[0])):
                total += matrix_a[i][k] * matrix_b[k][j]
            result[i][j] = total
    return result


def transpose_main_diagonal(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]


def transpose_side_diagonal(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    return [[matrix[rows - 1 - j][cols - 1 - i] for j in range(rows)] for i in range(cols)]


def transpose_vertical(matrix):
    return [row[::-1] for row in matrix]


def transpose_horizontal(matrix):
    return matrix[::-1]


def get_matrix_minor(matrix, i, j):
    return [row[:j] + row[j + 1:] for row in matrix[:i] + matrix[i + 1:]]


def calculate_determinant(matrix):
    if len(matrix) != len(matrix[0]):
        return None

    if len(matrix) == 1:
        return matrix[0][0]
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][2 - 1]

    det = 0
    for c in range(len(matrix)):
        sign = (-1) ** c
        sub_det = calculate_determinant(get_matrix_minor(matrix, 0, c))
        det += sign * matrix[0][c] * sub_det
    return det


def inverse_matrix(matrix):
    det = calculate_determinant(matrix)
    if det is None or det == 0:
        return None

    if len(matrix) == 1:
        return [[1 / matrix[0][0]]]

    cofactors = []
    for r in range(len(matrix)):
        cofactor_row = []
        for c in range(len(matrix)):
            minor = get_matrix_minor(matrix, r, c)
            cofactor_row.append(((-1) ** (r + c)) * calculate_determinant(minor))
        cofactors.append(cofactor_row)

    adjugate = transpose_main_diagonal(cofactors)

    return multiply_by_constant(adjugate, 1 / det)



def handle_transpose():
    print("\n1. Main diagonal")
    print("2. Side diagonal")
    print("3. Vertical line")
    print("4. Horizontal line")
    try:
        choice = int(input("Your choice: > "))
    except ValueError:
        print("Invalid choice.")
        return

    matrix = read_matrix(prompt_size="Enter matrix size: > ")
    if matrix is None:
        print("Invalid matrix data.")
        return

    if choice == 1:
        res = transpose_main_diagonal(matrix)
    elif choice == 2:
        res = transpose_side_diagonal(matrix)
    elif choice == 3:
        res = transpose_vertical(matrix)
    elif choice == 4:
        res = transpose_horizontal(matrix)
    else:
        print("Unknown transposition option.")
        return

    print("The result is:")
    print_matrix(res)


def main():
    while True:
        print("\n1. Add matrices")
        print("2. Multiply matrix by a constant")
        print("3. Multiply matrices")
        print("4. Transpose matrix")
        print("5. Calculate a determinant")
        print("6. Inverse matrix")
        print("0. Exit")

        try:
            choice_str = input("Your choice: > ").strip()
            choice = int(choice_str)
        except ValueError:
            continue

        if choice == 0:
            break
        elif choice == 1:
            matrix_a = read_matrix("Enter size of first matrix: > ", "Enter first matrix:")
            matrix_b = read_matrix("Enter size of second matrix: > ", "Enter second matrix:")
            if matrix_a and matrix_b:
                res = add_matrices(matrix_a, matrix_b)
                if res:
                    print("The result is:")
                    print_matrix(res)
                else:
                    print("The operation cannot be performed.")
            else:
                print("The operation cannot be performed.")
        elif choice == 2:
            matrix = read_matrix("Enter size of matrix: > ", "Enter matrix:")
            try:
                const_str = input("Enter constant: > ").strip()
                const = float(const_str) if '.' in const_str else int(const_str)
                if matrix:
                    res = multiply_by_constant(matrix, const)
                    print("The result is:")
                    print_matrix(res)
            except ValueError:
                print("The operation cannot be performed.")
        elif choice == 3:
            matrix_a = read_matrix("Enter size of first matrix: > ", "Enter first matrix:")
            matrix_b = read_matrix("Enter size of second matrix: > ", "Enter second matrix:")
            if matrix_a and matrix_b:
                res = multiply_matrices(matrix_a, matrix_b)
                if res:
                    print("The result is:")
                    print_matrix(res)
                else:
                    print("The operation cannot be performed.")
            else:
                print("The operation cannot be performed.")
        elif choice == 4:
            handle_transpose()
        elif choice == 5:
            matrix = read_matrix("Enter matrix size: > ", "Enter matrix:")
            if matrix:
                det = calculate_determinant(matrix)
                if det is not None:
                    print("The result is:")
                    if isinstance(det, float) and det.is_integer():
                        print(int(det))
                    else:
                        print(det)
                else:
                    print("The operation cannot be performed (matrix must be square).")
        elif choice == 6:
            matrix = read_matrix("Enter matrix size: > ", "Enter matrix:")
            if matrix:
                res = inverse_matrix(matrix)
                if res:
                    print("The result is:")
                    print_matrix(res)
                else:
                    print("This matrix doesn't have an inverse.")


if __name__ == "__main__":
    main()