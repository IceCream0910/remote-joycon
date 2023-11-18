import tkinter as tk
import subprocess
from threading import Thread
import tkinter.messagebox as messagebox

class CommandExecutor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Joy-con")
        self.root.geometry("500x150")  # Adjusted the size for better display

        # 첫 번째 버튼 (왼쪽 절반)
        self.client_button = tk.Button(self.root, text="서버 시작하기", command=self.run_client, bg="#ff5e52", fg="white")
        self.client_button.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        # Text 위젯 생성 (ipconfig 및 콘솔 출력용)
        self.output_text = tk.Text(self.root, wrap="word", height=10, width=40)
        self.output_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # 행과 열 가중치를 설정하여 창 크기 조절 시 위젯 크기를 조절
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)


    def run_client(self):
        self.run_command("python client.py")
        self.run_command("cd web && python -m http.server 3000")
        messagebox.showinfo("서버 시작", "서버가 성공적으로 시작되었습니다.")

    def run_command(self, command):
        def run():
            try:
                result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
                output = result.stdout.strip()
                self.show_output(output)
            except subprocess.CalledProcessError as e:
                error_output = e.stderr.decode('utf-8').strip()
                self.show_output(f"Error:\n{error_output}")

        # 새 스레드에서 명령 실행
        Thread(target=run).start()

    def show_output(self, output):
        # 기존 텍스트 삭제 후 결과 추가
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, output)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    executor = CommandExecutor()
    executor.run()
