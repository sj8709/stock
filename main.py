import os

def main():
    print("🟢 Stock Manager")
    print("1. 티커 등록")
    print("2. 주가 수집 및 저장")
    choice = input("선택 (1 또는 2): ").strip()

    if choice == '1':
        os.system("python register_ticker.py")
    elif choice == '2':
        os.system("python fetch_and_save.py")
    else:
        print("❗ 잘못된 선택입니다.")

if __name__ == "__main__":
    main()