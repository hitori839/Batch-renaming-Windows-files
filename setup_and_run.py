import os
import sys
import winreg
import ctypes
from tkinter import Tk, Label, Entry, Button, messagebox

# 1. 관리자 권한 획득 확인
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# 2. 레지스트리 자동 등록 함수
def register_context_menu():
    exe_path = sys.executable  # 현재 실행 파일의 경로
    key_path = r"*\shell\BatchRename"
    
    try:
        # 우클릭 메뉴 이름 설정
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path) as key:
            winreg.SetValue(key, "", winreg.REG_SZ, "스마트 이름 바꾸기")
            
        # 명령어 연결 (여러 파일 처리를 위해 %1 사용)
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, f"{key_path}\\command") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, f'"{exe_path}" "%1"')
            
        messagebox.showinfo("완료", "우클릭 메뉴에 성공적으로 등록되었습니다!")
    except Exception as e:
        messagebox.showerror("오류", f"등록 실패: {e}")

# 3. 이름 바꾸기 UI 및 로직
def rename_ui(file_paths):
    root = Tk()
    root.title("이름 바꾸기 도구")
    root.geometry("300x150")

    Label(root, text="찾을 내용:").pack()
    search_entry = Entry(root)
    search_entry.pack()

    Label(root, text="바꿀 내용:").pack()
    replace_entry = Entry(root)
    replace_entry.pack()

    def apply_rename():
        search_text = search_entry.get()
        replace_text = replace_entry.get()
        
        for path in file_paths:
            if os.path.exists(path):
                dir_name = os.path.dirname(path)
                old_name = os.path.basename(path)
                new_name = old_name.replace(search_text, replace_text)
                os.rename(path, os.path.join(dir_name, new_name))
        
        messagebox.showinfo("성공", "변경 완료!")
        root.destroy()

    Button(root, text="변경하기", command=apply_rename).pack()
    root.mainloop()

# 메인 실행부
if __name__ == "__main__":
    # 파일 인자(우클릭으로 들어온 경로)가 있으면 이름 바꾸기 실행
    if len(sys.argv) > 1:
        rename_ui(sys.argv[1:])
    else:
        # 인자 없이 직접 실행했다면 '설정 모드'
        if is_admin():
            register_context_menu()
        else:
            # 관리자 권한으로 다시 실행 요청
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, None, None, 1)