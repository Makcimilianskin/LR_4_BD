import time

# Таблиця констант для S-блоку (таблиця заміни)
S_BOX = [0x3, 0x8, 0xF, 0x1, 0xA, 0x6, 0x5, 0xB,
         0x0, 0xE, 0x9, 0xD, 0x2, 0xC, 0x7, 0x4]

# Створення зворотної таблиці для S-блоку
S_BOX_INV = [0] * 16
for i, value in enumerate(S_BOX):
    S_BOX_INV[value] = i

# Таблиця перестановки для P-блоку
P_PERMUTATION = [1, 5, 2, 0, 3, 7, 4, 6]

# --- Функції для роботи з S-блоком ---

def encrypt_constants(input_byte):
    left_nibble = (input_byte >> 4) & 0xF
    right_nibble = input_byte & 0xF
    left_nibble_sub = S_BOX[left_nibble]
    right_nibble_sub = S_BOX[right_nibble]
    return (left_nibble_sub << 4) | right_nibble_sub

def decrypt_constants(output_byte):
    left_nibble = (output_byte >> 4) & 0xF
    right_nibble = output_byte & 0xF
    left_nibble_inv = S_BOX_INV[left_nibble]
    right_nibble_inv = S_BOX_INV[right_nibble]
    return (left_nibble_inv << 4) | right_nibble_inv

# --- Функції для роботи з P-блоком ---

def encrypt_permutation(input_byte):
    output_byte = 0
    for i, pos in enumerate(P_PERMUTATION):
        bit = (input_byte >> pos) & 1
        output_byte |= (bit << i)
    return output_byte

def decrypt_permutation(output_byte):
    input_byte = 0
    for i, pos in enumerate(P_PERMUTATION):
        bit = (output_byte >> i) & 1
        input_byte |= (bit << pos)
    return input_byte

# --- Функції для шифрування та дешифрування ---

def encrypt(input_byte):
    s_encrypted = encrypt_constants(input_byte)
    return encrypt_permutation(s_encrypted)

def decrypt(encrypted_byte):
    p_decrypted = decrypt_permutation(encrypted_byte)
    return decrypt_constants(p_decrypted)

# --- Тестування ---

def run_tests():
    print("\n--- Запуск тестів для всіх значень від 0 до 255 ---")
    all_tests_passed = True
    for i in range(256):
        encrypted = encrypt(i)
        decrypted = decrypt(encrypted)
        
        print(f"Тест {i}: Вхідне число: {i:02X} ({i:08b}), Зашифровано: {encrypted:02X} ({encrypted:08b}), Розшифровано: {decrypted:02X} ({decrypted:08b})", end=" ")

        if i != decrypted:
            print(f"❌ Тест не пройдено для значення {i:02X} (зашифровано: {encrypted:02X}, розшифровано: {decrypted:02X})")
            all_tests_passed = False
        else:
            print("✔️ Тест пройдено успішно.")
        
    if all_tests_passed:
        print("\n✔️ Усі тести пройдено успішно.")
    else:
        print("\n❌ Деякі тести не пройшли.")

# --- Відображення таблиць S і P-блоків ---

def display_s_block_table():
    print("\n--- Таблиця S-блоку (Заміна) ---")
    print("Вхід -> Вихід")
    for i, value in enumerate(S_BOX):
        print(f"{i:01X} -> {value:01X}")

def display_p_block_table():
    print("\n--- Таблиця P-блоку (Перестановка) ---")
    print("Позиція -> Перестановка")
    for i, pos in enumerate(P_PERMUTATION):
        print(f"{i} -> {pos}")

# --- Основна програма з меню ---

def main_menu():
    while True:
        print("\n--- Головне Меню ---")
        print("1. Шифрування та дешифрування")
        print("2. Тестування")
        print("3. Таблиця S-блоку")
        print("4. Таблиця P-блоку")
        print("5. Вихід")
        
        choice = input("Оберіть опцію (1-5): ")
        
        if choice == '1':
            encryption_menu()
        elif choice == '2':
            run_tests()
        elif choice == '3':
            display_s_block_table()
        elif choice == '4':
            display_p_block_table()
        elif choice == '5':
            print("Вихід з програми.")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

def encryption_menu():
    input_byte = int(input("Введіть 8-бітне число для шифрування (0-255): "))
    while True:
        print("\n--- Меню типу шифрування ---")
        print("1. Шифрування через S-блок")
        print("2. Шифрування через P-блок")
        print("3. Повне шифрування (S-блок + P-блок)")
        print("4. Повернутися в головне меню")
        
        enc_choice = input("Оберіть тип шифрування (1-4): ")
        
        if enc_choice == '1':
            encrypted = encrypt_constants(input_byte)
            print(f"Зашифровано (S-блок): {encrypted:08b} (десяткове: {encrypted})")
            decrypted = decrypt_constants(encrypted)
            print(f"Розшифровано (S-блок): {decrypted:08b} (десяткове: {decrypted})")
        elif enc_choice == '2':
            encrypted = encrypt_permutation(input_byte)
            print(f"Зашифровано (P-блок): {encrypted:08b} (десяткове: {encrypted})")
            decrypted = decrypt_permutation(encrypted)
            print(f"Розшифровано (P-блок): {decrypted:08b} (десяткове: {decrypted})")
        elif enc_choice == '3':
            encrypted = encrypt(input_byte)
            print(f"Повне шифрування: {encrypted:08b} (десяткове: {encrypted})")
            decrypted = decrypt(encrypted)
            print(f"Розшифровано: {decrypted:08b} (десяткове: {decrypted})")
        elif enc_choice == '4':
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main_menu()