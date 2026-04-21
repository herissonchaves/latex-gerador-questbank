import zipfile, os, re, shutil

TEX_PATH  = 'saida/questoes.tex'
MAIN_SRC  = 'main.tex'          # template na raiz do projeto
MAIN_DEST = 'saida/main.tex'
ZIP_PATH  = 'saida/questoes.zip'

# 1. Copiar main.tex (wrapper Overleaf) para saida/
shutil.copy(MAIN_SRC, MAIN_DEST)

# 2. Encontrar imagens referenciadas em questoes.tex
with open(TEX_PATH, encoding='utf-8') as f:
    tex = f.read()

imagens = list(dict.fromkeys(re.findall(r'\\imagem\{([^}]+)\}', tex)))

# 3. Localizar arquivos de imagem (busca em pastas comuns)
SEARCH_DIRS = ['.', 'saida', 'entrada', 'imagens']
found_imgs   = {}   # basename → caminho real
missing_imgs = []

for img in imagens:
    basename = os.path.basename(img)
    for d in SEARCH_DIRS:
        for candidate in [os.path.join(d, img), os.path.join(d, basename)]:
            if os.path.exists(candidate):
                found_imgs[basename] = candidate
                break
        if basename in found_imgs:
            break
    else:
        missing_imgs.append(img)

# 4. Montar o ZIP
with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.write(TEX_PATH,  'questoes.tex')   # DSL QuestBank (lido pelo app)
    zf.write(MAIN_DEST, 'main.tex')       # wrapper Overleaf (entrada do compilador)
    for basename, path in found_imgs.items():
        zf.write(path, basename)           # imagens na raiz do ZIP

print(f"✓ ZIP criado: {ZIP_PATH}")
print(f"  questoes.tex + main.tex + {len(found_imgs)} imagem(ns)")
if missing_imgs:
    print(f"\n⚠ Imagens NÃO encontradas ({len(missing_imgs)}) — adicione ao ZIP manualmente:")
    for m in missing_imgs:
        print(f"  - {m}")
