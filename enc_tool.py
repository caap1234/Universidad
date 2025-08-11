 #!/usr/bin/env python3
 """
 Uso:
   - Generar llave:
       python enc_tool.py genkey --out key.key
   - Cifrar archivo:
       python enc_tool.py encrypt --key key.key --in plain.txt --out plain.txt.enc
   - Descifrar archivo:
       python enc_tool.py decrypt --key key.key --in plain.txt.enc --out plain.txt.dec
   - Cifrar/descifrar texto corto (stdin/stdout):
       echo "mensaje" | python enc_tool.py encrypt --key key.key --text
       python enc_tool.py decrypt --key key.key --in - --text  # leer de stdin y mostrar texto descifrado
 """
 
 import argparse
 import sys
 from cryptography.fernet import Fernet, InvalidToken
 from pathlib import Path
 
 def gen_key(out_path: Path):
     key = Fernet.generate_key()
     out_path.write_bytes(key)
     print(f"[+] Llave generada y guardada en: {out_path}")
 
 def load_key(path: Path) -> bytes:
     if not path.exists():
         raise FileNotFoundError(f"No existe la llave: {path}")
     return path.read_bytes()
 
 def encrypt_file(key: bytes, in_file: Path, out_file: Path):
     f = Fernet(key)
     data = in_file.read_bytes()
     token = f.encrypt(data)
     out_file.write_bytes(token)
     print(f"[+] Cifrado: {in_file} -> {out_file} (bytes in: {len(data)}, bytes out: {len(token)})")
 
 def decrypt_file(key: bytes, in_file: Path, out_file: Path):
     f = Fernet(key)
     token = in_file.read_bytes()
     try:
         data = f.decrypt(token)
     except InvalidToken:
         print("[-] Error: llave incorrecta o datos corruptos (InvalidToken).", file=sys.stderr)
         sys.exit(2)
     out_file.write_bytes(data)
     print(f"[+] Descifrado: {in_file} -> {out_file} (bytes out: {len(data)})")
 
 def main():
     parser = argparse.ArgumentParser(description="Herramienta de cifrado simétrico (Fernet).")
     sub = parser.add_subparsers(dest="cmd", required=True)
 
     p_gen = sub.add_parser("genkey", help="Generar y guardar llave.")
     p_gen.add_argument("--out", required=True, type=Path, help="Archivo salida para la llave (ej: key.key)")
 
     p_enc = sub.add_parser("encrypt", help="Cifrar archivo o texto.")
     p_enc.add_argument("--key", required=True, type=Path, help="Archivo con llave")
     p_enc.add_argument("--in", dest="infile", required=True, type=Path, help="Archivo de entrada (usa - para stdin)
     p_enc.add_argument("--out", dest="outfile", required=True, type=Path, help="Archivo de salida")
     p_enc.add_argument("--text", action="store_true", help="Tratar entrada/salida como texto (utf-8) y mostrar por 
 ut si --out=-")
 
     p_dec = sub.add_parser("decrypt", help="Descifrar archivo o texto.")
     p_dec.add_argument("--key", required=True, type=Path, help="Archivo con llave")
     p_dec.add_argument("--in", dest="infile", required=True, type=Path, help="Archivo de entrada (usa - para stdin)
     p_dec.add_argument("--out", dest="outfile", required=True, type=Path, help="Archivo de salida")
     p_dec.add_argument("--text", action="store_true", help="Tratar entrada/salida como texto (utf-8) y mostrar por 
 ut si --out=-")
 
     args = parser.parse_args()
     if args.cmd == "genkey":
         gen_key(args.out)
         return
 
     key = load_key(args.key)
     if args.cmd == "encrypt":
         if str(args.infile) == "-":
             data = sys.stdin.buffer.read()
             f = Fernet(key)
             token = f.encrypt(data)
             if str(args.outfile) == "-":
                 sys.stdout.buffer.write(token)
             else:
                 args.outfile.write_bytes(token)
                 print(f"[+] Cifrado stdin -> {args.outfile} (bytes out: {len(token)})")
         else:
             encrypt_file(key, args.infile, args.outfile)
 
     elif args.cmd == "decrypt":
         if str(args.infile) == "-":
             token = sys.stdin.buffer.read()
             f = Fernet(key)
             try:
                 data = f.decrypt(token)
             except InvalidToken:
                 print("[-] Error: llave incorrecta o datos corruptos (InvalidToken).", file=sys.stderr)
                 sys.exit(2)
             if str(args.outfile) == "-":
                 sys.stdout.buffer.write(data)
             else:
                 args.outfile.write_bytes(data)
                 print(f"[+] Descifrado stdin -> {args.outfile} (bytes out: {len(data)})")
         else:
             decrypt_file(key, args.infile, args.outfile)
 
 if __name__ == "__main__":
     main()
