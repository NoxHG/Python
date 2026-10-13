# 📘 Manual do Dev Júnior — Pygame

Guia de consulta rápida para usar **durante o desenvolvimento**. Cada tópico traz: o que a função faz, a assinatura, um exemplo e, quando existir, a **fórmula** por trás.

> Referência: Pygame 2.x (também funciona no `pygame-ce`, o fork da comunidade). Itens exclusivos do `pygame-ce` estão marcados com **(CE)**.
> Documentação oficial: https://www.pygame.org/docs/

---

## 📑 Índice

1. [Instalação e primeiro programa](#1-instalação-e-primeiro-programa)
2. [Game loop, FPS e delta time](#2-game-loop-fps-e-delta-time)
3. [Janela e display](#3-janela-e-display)
4. [Cores](#4-cores)
5. [Surface (superfícies)](#5-surface-superfícies)
6. [Desenhando na tela: pygame.draw](#6-desenhando-na-tela-pygamedraw)
7. [Rect: retângulos](#7-rect-retângulos)
8. [Imagens e transformações](#8-imagens-e-transformações)
9. [Texto e fontes](#9-texto-e-fontes)
10. [Eventos](#10-eventos)
11. [Teclado](#11-teclado)
12. [Mouse](#12-mouse)
13. [Joystick / Controle](#13-joystick--controle)
14. [Vetores: pygame.math](#14-vetores-pygamemath)
15. [Movimento e física (fórmulas)](#15-movimento-e-física-fórmulas)
16. [Colisões: funções e fórmulas](#16-colisões-funções-e-fórmulas)
17. [Sprites e Groups](#17-sprites-e-groups)
18. [Máscaras (colisão pixel perfect)](#18-máscaras-colisão-pixel-perfect)
19. [Áudio: mixer](#19-áudio-mixer)
20. [Tempo, timers e cooldowns](#20-tempo-timers-e-cooldowns)
21. [Animação por frames e spritesheet](#21-animação-por-frames-e-spritesheet)
22. [Câmera e scroll](#22-câmera-e-scroll)
23. [Tilemap (mapas de blocos)](#23-tilemap-mapas-de-blocos)
24. [Interpolação e easing](#24-interpolação-e-easing)
25. [Interface: botões, barras e texto digitado](#25-interface-botões-barras-e-texto-digitado)
26. [Cenas e estados de jogo](#26-cenas-e-estados-de-jogo)
27. [Salvar e carregar dados](#27-salvar-e-carregar-dados)
28. [Performance](#28-performance)
29. [Empacotar o jogo (.exe)](#29-empacotar-o-jogo-exe)
30. [Erros comuns e boas práticas](#30-erros-comuns-e-boas-práticas)
31. [Cheat sheet de fórmulas](#31-cheat-sheet-de-fórmulas)
32. [Template completo de jogo](#32-template-completo-de-jogo)

---

## 1. Instalação e primeiro programa

```bash
pip install pygame          # versão oficial
# ou
pip install pygame-ce       # fork da comunidade (não instale os dois juntos!)

python -m pygame.examples.aliens   # testa se funcionou
```

Programa mínimo:

```python
import pygame

pygame.init()                               # inicializa todos os módulos
tela = pygame.display.set_mode((800, 600))  # cria a janela
pygame.display.set_caption("Meu jogo")
clock = pygame.time.Clock()

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    tela.fill((30, 30, 30))                 # limpa a tela
    pygame.display.flip()                   # mostra o que foi desenhado
    clock.tick(60)                          # limita a 60 FPS

pygame.quit()
```

| Função | O que faz |
|---|---|
| `pygame.init()` | Inicializa todos os módulos. Retorna `(ok, falhas)`. |
| `pygame.quit()` | Desliga todos os módulos. Chame no final. |
| `pygame.get_init()` | `True` se o pygame está inicializado. |
| `pygame.get_error()` | Última mensagem de erro do SDL. |
| `pygame.version.ver` | Versão do pygame (ex.: `"2.6.1"`). |
| `pygame.version.SDL` | Versão do SDL. |

---

## 2. Game loop, FPS e delta time

Todo jogo repete **3 passos** a cada quadro (frame):

1. **Eventos** (input do jogador)
2. **Atualizar** (lógica, física, colisões)
3. **Desenhar** (renderizar)

### Delta time (dt)

`clock.tick(fps)` devolve os **milissegundos** desde a chamada anterior. Use isso para o jogo rodar na mesma velocidade em qualquer computador.

```python
clock = pygame.time.Clock()
FPS = 60

while rodando:
    dt = clock.tick(FPS) / 1000      # segundos desde o último frame (ex.: 0.0166)
    ...
    jogador.x += velocidade * dt     # velocidade em PIXELS POR SEGUNDO
```

**Fórmulas**

```
dt (s)       = ms_do_frame / 1000
deslocamento = velocidade (px/s) × dt (s)
FPS          = 1000 / ms_do_frame
ms_por_frame = 1000 / FPS            (60 FPS ≈ 16,67 ms)
```

| Método | O que faz |
|---|---|
| `clock.tick(fps)` | Espera para manter o FPS e retorna ms do frame. |
| `clock.tick_busy_loop(fps)` | Mais preciso, mas gasta CPU. |
| `clock.get_fps()` | FPS médio (últimos 10 frames). |
| `clock.get_time()` | ms do frame anterior (o mesmo valor que o `tick` retornou). |

> ⚠️ Se a janela for arrastada ou travar, `dt` pode ficar enorme. Limite: `dt = min(dt, 0.05)`.

---

## 3. Janela e display

```python
tela = pygame.display.set_mode((largura, altura), flags=0, depth=0, display=0, vsync=0)
```

| Flag | Efeito |
|---|---|
| `pygame.FULLSCREEN` | Tela cheia. |
| `pygame.RESIZABLE` | Usuário pode redimensionar a janela. |
| `pygame.NOFRAME` | Sem bordas/barra de título. |
| `pygame.SCALED` | Escala a resolução lógica para caber na janela (ótimo para pixel art). |
| `pygame.DOUBLEBUF` | Buffer duplo. |
| `pygame.OPENGL` | Usa contexto OpenGL. |

Combine com `|`: `pygame.SCALED | pygame.FULLSCREEN`.
`vsync=1` só funciona com `SCALED` ou `OPENGL`.

| Função | Descrição |
|---|---|
| `pygame.display.flip()` | Atualiza **a tela inteira**. |
| `pygame.display.update(rect_ou_lista)` | Atualiza só as áreas informadas (sem argumento = tela inteira). |
| `pygame.display.set_caption("Título")` | Título da janela. |
| `pygame.display.set_icon(surface)` | Ícone da janela (chame **antes** do `set_mode`). |
| `pygame.display.get_surface()` | Retorna a Surface da tela atual. |
| `pygame.display.toggle_fullscreen()` | Alterna tela cheia. |
| `pygame.display.get_window_size()` | Tamanho real da janela. |
| `pygame.display.list_modes()` | Resoluções suportadas. |
| `pygame.display.Info()` | Info do monitor: `.current_w`, `.current_h`. |
| `pygame.display.get_desktop_sizes()` | Lista com tamanho de cada monitor. |

**Resolução fixa com escala (pixel art)**

```python
tela = pygame.display.set_mode((320, 180), pygame.SCALED | pygame.RESIZABLE)
```

**Fórmula de proporção (aspect ratio)**

```
escala = min(janela_w / base_w, janela_h / base_h)
novo_w = base_w × escala
novo_h = base_h × escala
offset_x = (janela_w - novo_w) / 2      # barras pretas laterais
offset_y = (janela_h - novo_h) / 2
```

---

## 4. Cores

Cores são tuplas **RGB** `(0–255, 0–255, 0–255)` ou **RGBA** (com transparência).

```python
BRANCO   = (255, 255, 255)
PRETO    = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE    = (0, 255, 0)
AZUL     = (0, 0, 255)
AMARELO  = (255, 255, 0)
TRANSPARENTE = (0, 0, 0, 0)
```

Classe `pygame.Color`:

```python
c = pygame.Color(255, 100, 0)
c = pygame.Color("red")        # por nome
c = pygame.Color("#ff6400")    # hexadecimal
c.r, c.g, c.b, c.a             # canais
c.hsva = (200, 80, 100, 100)   # H(0-360) S V A (0-100)
c.lerp((0, 0, 255), 0.5)       # mistura 50% com azul
```

**Fórmulas**

```
Mistura:        cor = c1 + (c2 - c1) × t        (t de 0 a 1, por canal)
Escurecer:      cor = (r × f, g × f, b × f)     (f entre 0 e 1)
Clarear:        cor = (r + (255-r) × f, ...)
Tons de cinza:  cinza = 0.299×R + 0.587×G + 0.114×B
Cor aleatória:  (randint(0,255), randint(0,255), randint(0,255))
```

---

## 5. Surface (superfícies)

Toda imagem, tela e texto é uma `Surface`. A tela (`display`) é a Surface principal.

```python
s = pygame.Surface((100, 50))                       # sem transparência por pixel
s = pygame.Surface((100, 50), pygame.SRCALPHA)      # COM transparência por pixel
```

| Método | Descrição |
|---|---|
| `s.fill(cor, rect=None)` | Preenche (toda ou uma área). |
| `s.blit(origem, destino, area=None, special_flags=0)` | Cola outra Surface. `destino` é `(x, y)` ou um Rect (usa o topleft). |
| `s.blits([(surf, pos), ...])` | Vários blits de uma vez (mais rápido). |
| `s.convert()` | Converte p/ o formato da tela (mais rápido, **sem alfa**). |
| `s.convert_alpha()` | Converte mantendo transparência. **Use ao carregar PNG.** |
| `s.copy()` | Cópia independente. |
| `s.subsurface(rect)` | Recorte que **compartilha** pixels com a original. |
| `s.get_rect(**kw)` | Rect do tamanho da Surface: `s.get_rect(center=(400,300))`. |
| `s.get_size()`, `get_width()`, `get_height()` | Dimensões. |
| `s.set_colorkey(cor)` | Torna uma cor transparente. |
| `s.set_alpha(0-255)` | Opacidade da Surface inteira (0 = invisível). |
| `s.get_at((x, y))` / `s.set_at((x, y), cor)` | Lê/escreve um pixel (lento em loops grandes). |
| `s.set_clip(rect)` / `s.get_clip()` | Limita a área onde se pode desenhar. |
| `s.scroll(dx, dy)` | Desloca o conteúdo da Surface. |
| `s.get_bounding_rect()` | Menor Rect que contém os pixels não transparentes. |

**Blend (modos de mistura)** via `special_flags`:

```python
tela.blit(luz, pos, special_flags=pygame.BLEND_RGB_ADD)    # clareia (efeito de luz)
tela.blit(sombra, pos, special_flags=pygame.BLEND_RGB_MULT) # escurece
```

Flags: `BLEND_RGB_ADD`, `BLEND_RGB_SUB`, `BLEND_RGB_MULT`, `BLEND_RGB_MIN`, `BLEND_RGB_MAX`, e as versões `BLEND_RGBA_*`.

**Fórmula de posicionamento**

```
Centralizar:   x = (tela_w - surf_w) / 2        y = (tela_h - surf_h) / 2
(ou use get_rect(center=...))
```

---

## 6. Desenhando na tela: pygame.draw

Todas retornam um `Rect` com a área alterada. Parâmetro `width`: `0` = preenchido; `>0` = só contorno com essa espessura.

| Função | Assinatura |
|---|---|
| Retângulo | `pygame.draw.rect(surf, cor, rect, width=0, border_radius=0)` |
| Círculo | `pygame.draw.circle(surf, cor, centro, raio, width=0)` |
| Elipse | `pygame.draw.ellipse(surf, cor, rect, width=0)` |
| Linha | `pygame.draw.line(surf, cor, ponto_a, ponto_b, width=1)` |
| Várias linhas | `pygame.draw.lines(surf, cor, fechado, [pontos], width=1)` |
| Linha suave | `pygame.draw.aaline(surf, cor, ponto_a, ponto_b)` |
| Linhas suaves | `pygame.draw.aalines(surf, cor, fechado, [pontos])` |
| Polígono | `pygame.draw.polygon(surf, cor, [pontos], width=0)` |
| Arco | `pygame.draw.arc(surf, cor, rect, ang_ini, ang_fim, width=1)` (ângulos em **radianos**) |

Exemplos:

```python
pygame.draw.rect(tela, (200, 50, 50), (100, 100, 200, 80))             # (x, y, w, h)
pygame.draw.rect(tela, (255, 255, 255), (100, 100, 200, 80), 3)        # só borda
pygame.draw.rect(tela, (50, 50, 200), (100, 200, 200, 80), border_radius=15)  # cantos redondos
pygame.draw.circle(tela, (0, 255, 0), (400, 300), 40)
pygame.draw.line(tela, (255, 255, 0), (0, 0), (800, 600), 4)
pygame.draw.polygon(tela, (255, 0, 255), [(400, 100), (450, 200), (350, 200)])  # triângulo
pygame.draw.lines(tela, (255, 255, 255), True, [(10,10), (100,10), (100,100)], 2)
```

**Fórmulas úteis para desenho**

```
Ponto no círculo:      x = cx + r × cos(θ)        y = cy + r × sin(θ)       (θ em radianos)
Graus → radianos:      rad = graus × π / 180      (math.radians)
Radianos → graus:      graus = rad × 180 / π      (math.degrees)
Polígono regular (n lados): para i em 0..n-1:
                       θ = 2π × i / n
                       ponto = (cx + r×cos θ, cy + r×sin θ)
Estrela (2n pontos):   alterne raio externo R e interno r a cada passo de π/n
Barra de vida:         largura_atual = largura_max × (vida / vida_max)
```

```python
import math
def poligono(cx, cy, r, n, rot=0):
    return [(cx + r*math.cos(rot + 2*math.pi*i/n),
             cy + r*math.sin(rot + 2*math.pi*i/n)) for i in range(n)]
```

> 💡 O eixo **Y cresce para baixo** no Pygame. A origem `(0, 0)` é o canto superior esquerdo.

---

## 7. Rect: retângulos

`pygame.Rect(x, y, largura, altura)` — guarda **inteiros** (a parte decimal é cortada). Para posição decimal, guarde `x`/`y` em `float` ou `Vector2` separado e copie para o rect. **(CE)** tem `pygame.FRect` com floats.

### Atributos (todos podem ser lidos **e atribuídos**)

```
x, y, w, h  (ou width, height)
top, left, bottom, right
topleft, topright, bottomleft, bottomright
midtop, midleft, midbottom, midright
center, centerx, centery
size
```

```python
r = pygame.Rect(100, 100, 50, 30)
r.center = (400, 300)       # move o rect pelo centro
r.bottom = 580              # "pés" do personagem no chão
r.right = tela.get_width()  # encosta na direita
```

### Métodos

| Método | Descrição |
|---|---|
| `move(dx, dy)` / `move_ip(dx, dy)` | Retorna cópia movida / move o próprio (`ip` = in place). |
| `inflate(dw, dh)` / `inflate_ip` | Aumenta (ou diminui se negativo) mantendo o centro. |
| `scale_by(f)` **(CE)** | Escala o rect por um fator. |
| `clamp(outro)` / `clamp_ip` | Move o rect para **dentro** de outro. |
| `clip(outro)` | Retorna a área de **interseção**. |
| `union(outro)` | Menor rect que contém os dois. |
| `unionall([rects])` | União de vários. |
| `fit(outro)` | Ajusta mantendo proporção para caber em outro. |
| `normalize()` | Corrige largura/altura negativas. |
| `contains(outro)` | `True` se `outro` está totalmente dentro. |
| `collidepoint(x, y)` | Ponto dentro do rect? |
| `colliderect(outro)` | Dois rects se sobrepõem? |
| `collidelist(lista)` | Índice do 1º rect da lista que colide (ou `-1`). |
| `collidelistall(lista)` | Lista de índices que colidem. |
| `collidedict(dict)` / `collidedictall` | Idem, com dicionário. |
| `clipline(a, b)` | Parte de uma linha que está dentro do rect. |

**Manter o jogador dentro da tela**

```python
jogador_rect.clamp_ip(tela.get_rect())
```

**Fórmulas**

```
right   = x + w            bottom = y + h
centerx = x + w / 2        centery = y + h / 2
área    = w × h
```

---

## 8. Imagens e transformações

### Carregar e salvar

```python
img = pygame.image.load("assets/player.png").convert_alpha()   # PNG com transparência
fundo = pygame.image.load("assets/fundo.jpg").convert()        # imagem sem transparência
pygame.image.save(tela, "print.png")                           # screenshot
```

> ⚠️ Carregue as imagens **uma única vez**, fora do loop principal.

### Caminho de arquivos seguro

```python
from pathlib import Path
BASE = Path(__file__).parent
img = pygame.image.load(BASE / "assets" / "player.png").convert_alpha()
```

### pygame.transform

| Função | Descrição |
|---|---|
| `transform.scale(surf, (w, h))` | Redimensiona (rápido, serrilhado — bom p/ pixel art). |
| `transform.smoothscale(surf, (w, h))` | Redimensiona suavizado (requer 24/32 bits). |
| `transform.scale_by(surf, fator)` **(CE / 2.1.3+)** | Escala por fator. |
| `transform.rotate(surf, angulo)` | Gira em **graus, sentido anti-horário**. A imagem cresce (canto vazio). |
| `transform.rotozoom(surf, angulo, escala)` | Gira + escala com suavização. |
| `transform.flip(surf, flip_x, flip_y)` | Espelha horizontal/vertical. |
| `transform.chop(surf, rect)` | Remove uma área. |
| `transform.average_color(surf)` | Cor média. |
| `transform.threshold(...)` | Substitui cores próximas a uma cor-alvo. |

**Girar mantendo o centro (muito comum)**

```python
original = img                         # guarde sempre a original!
girada = pygame.transform.rotate(original, angulo)
rect = girada.get_rect(center=posicao)
tela.blit(girada, rect)
```

> ⚠️ Nunca gire a imagem já girada (perde qualidade). Gire sempre a original.

**Fórmulas**

```
Proporção:         nova_h = nova_w × (altura / largura)
Escala por fator:  novo_tamanho = (int(w × f), int(h × f))
Ângulo apontando p/ o mouse (para transform.rotate, anti-horário, Y invertido):
    dx = mouse_x - obj_x
    dy = mouse_y - obj_y
    angulo = math.degrees(math.atan2(-dy, dx))
Com Vector2:   angulo = Vector2(1, 0).angle_to(alvo - pos)  # graus, horário na tela (Y para baixo)
```

### Espelhar o personagem conforme a direção

```python
img_atual = img if olhando_direita else pygame.transform.flip(img, True, False)
```

---

## 9. Texto e fontes

```python
fonte = pygame.font.Font(None, 36)                 # fonte padrão, tamanho 36
fonte = pygame.font.Font("assets/minha.ttf", 36)   # arquivo .ttf próprio
fonte = pygame.font.SysFont("arial", 36, bold=True, italic=False)  # fonte do sistema

texto = fonte.render("Pontos: 10", True, (255, 255, 255))    # (texto, antialias, cor, fundo=None)
tela.blit(texto, (10, 10))
```

| Função / método | Descrição |
|---|---|
| `font.render(txt, antialias, cor, fundo=None)` | Retorna uma Surface com o texto (1 linha). |
| `font.size(txt)` | Retorna `(largura, altura)` sem renderizar. |
| `font.get_linesize()` | Altura recomendada de uma linha. |
| `font.set_bold(True)`, `set_italic`, `set_underline` | Estilos. |
| `pygame.font.get_fonts()` | Lista fontes do sistema. |
| `pygame.font.match_font("arial")` | Caminho da fonte. |

**Centralizar texto**

```python
rect = texto.get_rect(center=(400, 300))
tela.blit(texto, rect)
```

**Texto com quebra de linha (função pronta)**

```python
def desenhar_texto_multilinha(surf, texto, fonte, cor, rect, espaco=4):
    palavras = texto.split(" ")
    linha, y = "", rect.top
    for p in palavras:
        teste = f"{linha} {p}".strip()
        if fonte.size(teste)[0] <= rect.width:
            linha = teste
        else:
            surf.blit(fonte.render(linha, True, cor), (rect.left, y))
            y += fonte.get_linesize() + espaco
            linha = p
    surf.blit(fonte.render(linha, True, cor), (rect.left, y))
```

> 💡 `render` é caro. Se o texto não muda a cada frame, renderize **uma vez** e guarde a Surface (cache). `Font.render` também aceita `wraplength` em versões novas (pygame 2.1.4+/CE).

Para texto avançado, veja `pygame.freetype` (`pygame.freetype.SysFont`, `render_to`).

---

## 10. Eventos

```python
for evento in pygame.event.get():       # pega e esvazia a fila
    if evento.type == pygame.QUIT:
        rodando = False
    elif evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_ESCAPE:
            rodando = False
```

### Tipos principais

| Evento | Atributos | Quando acontece |
|---|---|---|
| `QUIT` | — | Clique no X da janela. |
| `KEYDOWN` / `KEYUP` | `key`, `mod`, `unicode`, `scancode` | Tecla pressionada/solta (**1 vez**). |
| `MOUSEMOTION` | `pos`, `rel`, `buttons` | Mouse se moveu. |
| `MOUSEBUTTONDOWN` / `UP` | `pos`, `button` (1=esq, 2=meio, 3=dir) | Clique. |
| `MOUSEWHEEL` | `x`, `y` (`y`>0 = rolou para cima) | Roda do mouse. |
| `TEXTINPUT` | `text` | Texto digitado (respeita idioma/acentos). |
| `VIDEORESIZE` | `w`, `h`, `size` | Janela redimensionada. |
| `WINDOWFOCUSLOST` / `WINDOWFOCUSGAINED` | — | Janela perdeu/ganhou foco. |
| `JOYAXISMOTION`, `JOYBUTTONDOWN`, `JOYHATMOTION` | veja §13 | Controle. |
| `USEREVENT` … | `dict` livre | Eventos customizados. |

### Funções do módulo `pygame.event`

| Função | Descrição |
|---|---|
| `event.get(tipos=None)` | Retorna todos os eventos (pode filtrar por tipo). |
| `event.poll()` | Um evento por vez (ou `NOEVENT`). |
| `event.wait()` | Bloqueia até chegar um evento. |
| `event.pump()` | Atualiza estado interno se você **não** usa `get()`. |
| `event.clear()` | Descarta eventos. |
| `event.post(Event(...))` | Insere um evento na fila. |
| `event.Event(tipo, **dados)` | Cria um evento. |
| `event.set_blocked(tipo)` / `set_allowed` | Ignora/permite tipos de evento. |

### Evento customizado

```python
INIMIGO_SPAWN = pygame.USEREVENT + 1
pygame.time.set_timer(INIMIGO_SPAWN, 2000)      # a cada 2 s

for e in pygame.event.get():
    if e.type == INIMIGO_SPAWN:
        criar_inimigo()

pygame.event.post(pygame.event.Event(INIMIGO_SPAWN))  # disparo manual
```

> 🔑 **KEYDOWN** = acontece uma vez ao apertar (ótimo para pular, atirar, abrir menu).
> **get_pressed()** = verdadeiro enquanto segura (ótimo para andar).

---

## 11. Teclado

### Estado contínuo

```python
teclas = pygame.key.get_pressed()
if teclas[pygame.K_LEFT]  or teclas[pygame.K_a]: dx = -1
if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]: dx = +1
```

### Constantes de teclas comuns

```
Letras:       K_a ... K_z          Números:  K_0 ... K_9
Setas:        K_UP, K_DOWN, K_LEFT, K_RIGHT
Especiais:    K_SPACE, K_RETURN, K_ESCAPE, K_TAB, K_BACKSPACE, K_DELETE
Modificadoras:K_LSHIFT, K_RSHIFT, K_LCTRL, K_RCTRL, K_LALT, K_RALT
Funções:      K_F1 ... K_F12
Teclado num.: K_KP0 ... K_KP9, K_KP_ENTER
```

| Função | Descrição |
|---|---|
| `key.get_pressed()` | Estado de todas as teclas. |
| `key.get_mods()` | Modificadores ativos: `if pygame.key.get_mods() & pygame.KMOD_SHIFT:` |
| `key.set_repeat(delay_ms, intervalo_ms)` | Gera KEYDOWN repetido ao segurar. `set_repeat()` desliga. |
| `key.name(key)` | Nome da tecla (`"space"`). |
| `key.start_text_input()` / `stop_text_input()` | Liga/desliga evento `TEXTINPUT`. |

### Movimento 8 direções sem acelerar na diagonal

```python
direcao = pygame.Vector2(
    teclas[pygame.K_d] - teclas[pygame.K_a],
    teclas[pygame.K_s] - teclas[pygame.K_w],
)
if direcao.length_squared() > 0:
    direcao = direcao.normalize()
pos += direcao * velocidade * dt
```

**Fórmula (por que normalizar):** na diagonal `(1, 1)` o comprimento é `√2 ≈ 1,41`, ou seja, 41% mais rápido. Normalizar divide por esse comprimento:

```
v_normalizado = v / |v|          |v| = √(x² + y²)
```

### Combos / atalhos

```python
for e in pygame.event.get():
    if e.type == pygame.KEYDOWN and e.key == pygame.K_s and (e.mod & pygame.KMOD_CTRL):
        salvar()
```

---

## 12. Mouse

| Função | Descrição |
|---|---|
| `mouse.get_pos()` | `(x, y)` atual. |
| `mouse.get_pressed(3)` | `(esq, meio, dir)` — booleanos enquanto segura. |
| `mouse.get_rel()` | Deslocamento desde a última chamada. |
| `mouse.set_pos((x, y))` | Move o cursor. |
| `mouse.set_visible(False)` | Esconde o cursor. |
| `mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)` | Troca o cursor do sistema. |
| `mouse.get_focused()` | A janela tem o foco do mouse? |
| `event.set_grab(True)` | Prende o mouse na janela. |

```python
mx, my = pygame.mouse.get_pos()
if retangulo.collidepoint(mx, my):
    cor = COR_HOVER
if pygame.mouse.get_pressed()[0]:      # botão esquerdo segurado
    ...
```

**Cursor personalizado**

```python
pygame.mouse.set_visible(False)
...
tela.blit(cursor_img, cursor_img.get_rect(center=pygame.mouse.get_pos()))
```

**Fórmulas**

```
Mouse no mundo (com câmera):     mundo = mouse + camera_offset
Mouse com tela escalada:         logico = mouse_real / escala - offset
Direção até o mouse:             d = (mouse - pos).normalize()
Distância até o mouse:           (mouse - pos).length()
```

---

## 13. Joystick / Controle

```python
pygame.joystick.init()
controles = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

# no loop:
for e in pygame.event.get():
    if e.type == pygame.JOYBUTTONDOWN:
        print("Botão", e.button)
    if e.type == pygame.JOYDEVICEADDED:
        controles.append(pygame.joystick.Joystick(e.device_index))

if controles:
    j = controles[0]
    eixo_x = j.get_axis(0)       # -1.0 a +1.0
    eixo_y = j.get_axis(1)
    if abs(eixo_x) < 0.15: eixo_x = 0     # ZONA MORTA (deadzone)
    botao_a = j.get_button(0)
    hat = j.get_hat(0)           # (-1/0/1, -1/0/1) = D-pad
```

| Método | Descrição |
|---|---|
| `Joystick.get_name()` | Nome do controle. |
| `get_numaxes()`, `get_numbuttons()`, `get_numhats()` | Quantidades. |
| `get_axis(i)` | Valor de um eixo (-1 a 1). |
| `get_button(i)` | Botão pressionado? |
| `get_hat(i)` | D-pad. |
| `rumble(baixa, alta, ms)` | Vibração (se suportado). |

**Fórmula da zona morta radial**

```
magnitude = √(x² + y²)
se magnitude < deadzone: x = y = 0
```

---

## 14. Vetores: pygame.math

`Vector2` (2D) e `Vector3` (3D). Aceitam `+`, `-`, `*` por número, `/` por número, `==` e índices `v[0]`, `v.x`.

```python
from pygame.math import Vector2
pos = Vector2(100, 200)
vel = Vector2(3, -1)
pos += vel * dt
```

| Método / atributo | Descrição | Fórmula |
|---|---|---|
| `v.length()` / `v.magnitude()` | Comprimento | `√(x² + y²)` |
| `v.length_squared()` | Comprimento ao quadrado (**mais rápido**) | `x² + y²` |
| `v.normalize()` / `normalize_ip()` | Vetor unitário (comprimento 1) | `v / |v|` |
| `v.scale_to_length(n)` | Muda o comprimento mantendo a direção | `v / |v| × n` |
| `v.distance_to(o)` | Distância até outro ponto | `√((x₂-x₁)² + (y₂-y₁)²)` |
| `v.distance_squared_to(o)` | Distância² (mais rápida) | `dx² + dy²` |
| `v.dot(o)` | Produto escalar | `x₁x₂ + y₁y₂` |
| `v.cross(o)` | Produto vetorial 2D (escalar) | `x₁y₂ - y₁x₂` |
| `v.angle_to(o)` | Ângulo (graus) de `v` até `o` | — |
| `v.rotate(graus)` / `rotate_ip` / `rotate_rad` | Rotaciona | `x' = x cosθ - y sinθ`, `y' = x sinθ + y cosθ` |
| `v.reflect(normal)` | Reflete numa superfície (`normal` unitária) | `v - 2(v·n)n` |
| `v.project(o)` | Projeção de `v` sobre `o` | `(v·o / o·o) × o` |
| `v.lerp(o, t)` | Interpolação linear | `v + (o - v) × t` |
| `v.slerp(o, t)` | Interpolação esférica | — |
| `v.as_polar()` | `(raio, ângulo em graus)` | — |
| `v.from_polar((r, ang))` | Constrói a partir de polar | `(r cos θ, r sin θ)` |
| `v.update(x, y)` | Redefine valores | — |
| `v.copy()` | Cópia | — |
| `v.elementwise()` | Operações componente a componente | — |

> 💡 Use **`length_squared`** e **`distance_squared_to`** para comparar distâncias (evita a raiz quadrada):
> `if (a - b).length_squared() < raio * raio:`

### Pegar a posição decimal e usar no Rect

```python
pos = Vector2(100.0, 100.0)          # posição "real" com decimais
rect.center = pos                    # o rect arredonda sozinho
```

---

## 15. Movimento e física (fórmulas)

### 15.1 Movimento uniforme

```
posição = posição + velocidade × dt
```

```python
x += vx * dt
y += vy * dt
```

### 15.2 Aceleração e atrito

```
velocidade = velocidade + aceleração × dt
posição    = posição + velocidade × dt
```

```python
# Movimento com aceleração e atrito (top-down)
ACEL = 1500           # px/s²
ATRITO = 8            # quanto maior, mais rápido para
vel += direcao * ACEL * dt
vel -= vel * min(1, ATRITO * dt)       # atrito proporcional (independente de FPS)
if vel.length() > VEL_MAX:
    vel.scale_to_length(VEL_MAX)
pos += vel * dt
```

### 15.3 Gravidade e pulo (plataforma)

```
vy = vy + g × dt
y  = y + vy × dt
```

Fórmulas de pulo (Y para baixo, então a velocidade de pulo é **negativa**):

```
Velocidade inicial para atingir altura h:     v₀ = -√(2 × g × h)
Tempo até o ponto mais alto:                  t = |v₀| / g
Altura máxima com v₀ conhecido:               h = v₀² / (2g)
Gravidade para altura h e tempo t_subida:     g = 2h / t²      v₀ = -2h / t
Tempo total no ar (sobe e desce):             2 × |v₀| / g
Alcance horizontal do pulo:                   vx × tempo_total
```

```python
GRAVIDADE = 2000
ALTURA_PULO = 120
V_PULO = -(2 * GRAVIDADE * ALTURA_PULO) ** 0.5

vy += GRAVIDADE * dt
if pulou and no_chao:
    vy = V_PULO
y += vy * dt
```

**Melhorias comuns de plataforma:**

```python
# Coyote time: permite pular logo depois de sair da plataforma (~0,1 s)
# Jump buffer: lembra o botão de pulo apertado um pouco ANTES de tocar o chão
# Pulo variável: se soltou o botão e ainda está subindo → vy *= 0.5
# Velocidade terminal: vy = min(vy, VY_MAX)
```

### 15.4 Projétil (movimento balístico)

```
x(t) = x₀ + vx × t
y(t) = y₀ + vy × t + ½ × g × t²

Componentes de lançamento:  vx = v × cos(θ)      vy = -v × sin(θ)
```

### 15.5 Mover em direção a um alvo

```python
direcao = alvo - pos
dist = direcao.length()
if dist > 1:
    pos += direcao.normalize() * min(velocidade * dt, dist)   # não ultrapassa o alvo
```

### 15.6 Movimento por ângulo

```
vx = velocidade × cos(θ)
vy = velocidade × sin(θ)       (θ em radianos; sinal de vy depende do eixo Y)
```

```python
vel = Vector2(1, 0).rotate(angulo_graus) * velocidade
```

### 15.7 Movimento circular / órbita

```
x = cx + r × cos(ω × t)
y = cy + r × sin(ω × t)         ω = 2π × frequência   (rad/s)
```

### 15.8 Movimento oscilante (flutuar, pulsar)

```
y = y₀ + A × sin(2π × f × t)       A = amplitude   f = frequência (Hz)
```

```python
t = pygame.time.get_ticks() / 1000
y = y0 + 10 * math.sin(2 * math.pi * 0.5 * t)
```

### 15.9 Quique (bounce)

```python
if bola.left < 0 or bola.right > LARG:
    vx *= -1
if bola.top < 0 or bola.bottom > ALT:
    vy *= -1
# Com perda de energia:  vy = -vy × coef_restituicao   (0.6, por exemplo)
```

### 15.10 Rotação de um ponto ao redor de outro

```
x' = cx + (x - cx) × cosθ - (y - cy) × sinθ
y' = cy + (x - cx) × sinθ + (y - cy) × cosθ
```

Com vetor: `novo = centro + (ponto - centro).rotate(graus)`

### 15.11 Distância e ângulo entre dois pontos

```
dx = x₂ - x₁        dy = y₂ - y₁
distância = √(dx² + dy²)                  → math.hypot(dx, dy)
ângulo    = atan2(dy, dx)                 → math.atan2(dy, dx)  (radianos)
```

### 15.12 Ajuste de velocidade na diagonal

Veja §11 (normalização).

### 15.13 Valor limitado (clamp) e mapeamento

```
clamp(v, mín, máx) = max(mín, min(v, máx))
mapear(v, a1, b1, a2, b2) = a2 + (v - a1) × (b2 - a2) / (b1 - a1)
```

```python
def clamp(v, mn, mx): return max(mn, min(v, mx))
def mapear(v, a1, b1, a2, b2): return a2 + (v - a1) * (b2 - a2) / (b1 - a1)
```

### 15.14 Screen shake (tremor de tela)

```python
tremor = 8   # intensidade em px
offset = (random.randint(-tremor, tremor), random.randint(-tremor, tremor))
tremor = max(0, tremor - 30 * dt)       # decai com o tempo
# desenhe tudo em uma Surface "mundo" e faça tela.blit(mundo, offset)
```

---

## 16. Colisões: funções e fórmulas

### 16.1 Ponto × Retângulo

```
x >= rect.left  E  x < rect.right  E  y >= rect.top  E  y < rect.bottom
```

```python
rect.collidepoint(x, y)
```

### 16.2 Retângulo × Retângulo (AABB)

Dois retângulos alinhados aos eixos colidem **se** NÃO estão separados em nenhum eixo:

```
A.x < B.x + B.w   E   A.x + A.w > B.x
E
A.y < B.y + B.h   E   A.y + A.h > B.y
```

```python
a.colliderect(b)
a.collidelist([r1, r2, r3])        # índice do 1º que colidir, ou -1
a.collidelistall([r1, r2, r3])     # lista de índices
```

### 16.3 Círculo × Círculo

```
distância(c1, c2) <= r1 + r2
⇔ dx² + dy² <= (r1 + r2)²           (sem raiz → mais rápido)
```

```python
def colisao_circulos(p1, r1, p2, r2):
    return (Vector2(p1) - Vector2(p2)).length_squared() <= (r1 + r2) ** 2
```

### 16.4 Ponto × Círculo

```
(px - cx)² + (py - cy)² <= r²
```

### 16.5 Círculo × Retângulo

Ache o ponto do retângulo **mais próximo** do centro do círculo e compare:

```
px = clamp(cx, rect.left, rect.right)
py = clamp(cy, rect.top,  rect.bottom)
colidiu = (cx - px)² + (cy - py)² <= r²
```

```python
def circulo_x_rect(centro, raio, rect):
    px = max(rect.left, min(centro[0], rect.right))
    py = max(rect.top,  min(centro[1], rect.bottom))
    return (centro[0]-px)**2 + (centro[1]-py)**2 <= raio**2
```

### 16.6 Linha × Linha (raycast / tiro instantâneo)

Segmentos P1→P2 e P3→P4:

```
den = (x1-x2)(y3-y4) - (y1-y2)(x3-x4)
t   = ((x1-x3)(y3-y4) - (y1-y3)(x3-x4)) / den
u   = -((x1-x2)(y1-y3) - (y1-y2)(x1-x3)) / den
Colidem se den ≠ 0  E  0 ≤ t ≤ 1  E  0 ≤ u ≤ 1
Ponto de interseção = (x1 + t(x2-x1), y1 + t(y2-y1))
```

```python
def linha_x_linha(p1, p2, p3, p4):
    x1,y1 = p1; x2,y2 = p2; x3,y3 = p3; x4,y4 = p4
    den = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    if den == 0: return None            # paralelas
    t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / den
    u = -((x1-x2)*(y1-y3) - (y1-y2)*(x1-x3)) / den
    if 0 <= t <= 1 and 0 <= u <= 1:
        return (x1 + t*(x2-x1), y1 + t*(y2-y1))
    return None
```

Para linha × retângulo use `rect.clipline(a, b)` (retorna os pontos dentro do rect, ou `()`).

### 16.7 Raio de visão (linha de visão)

```python
for parede in paredes:
    if parede.clipline(olho, alvo):
        visivel = False
        break
```

### 16.8 Resolvendo a colisão (empurrar para fora)

**Profundidade de sobreposição:**

```
overlap_x = min(A.right, B.right)   - max(A.left, B.left)
overlap_y = min(A.bottom, B.bottom) - max(A.top,  B.top)
```

Empurre pelo eixo de **menor** sobreposição.

**Método mais simples e robusto: mova um eixo por vez**

```python
# Eixo X
jogador.x += vx * dt
for parede in paredes:
    if jogador.colliderect(parede):
        if vx > 0: jogador.right = parede.left
        elif vx < 0: jogador.left = parede.right

# Eixo Y
jogador.y += vy * dt
no_chao = False
for parede in paredes:
    if jogador.colliderect(parede):
        if vy > 0:
            jogador.bottom = parede.top
            no_chao = True
        elif vy < 0:
            jogador.top = parede.bottom
        vy = 0
```

> ⚠️ Como `Rect` guarda inteiros, mantenha a posição real em `Vector2`/`float` e copie para o rect antes de testar colisão.

### 16.9 Qual lado foi atingido?

```python
dx = (a.centerx - b.centerx) / b.width
dy = (a.centery - b.centery) / b.height
if abs(dx) > abs(dy):
    lado = "direita" if dx > 0 else "esquerda"
else:
    lado = "baixo" if dy > 0 else "cima"
```

### 16.10 Colisão de objetos rápidos (tunneling)

Objeto muito rápido pode **atravessar** parede fina entre dois frames. Soluções:

```
1. Dividir o movimento em passos:   passos = ceil(|deslocamento| / tamanho_min_do_obstáculo)
2. Testar um raio/linha da posição antiga até a nova (clipline)
3. Limitar a velocidade máxima
```

### 16.11 Colisão circular entre sprites e resposta (quique)

```
normal = (c2 - c1).normalize()
v_rel  = v1 - v2
se v_rel · normal > 0 (aproximando):
    v1' = v1 - (v_rel · normal) × normal       # massas iguais, colisão elástica
    v2' = v2 + (v_rel · normal) × normal
```

### 16.12 Colisão pixel perfect (máscaras)

Veja §18.

### 16.13 Colisão de sprites com Groups

Veja §17: `spritecollide`, `groupcollide`, `spritecollideany`, `collide_circle`, `collide_mask`.

### 16.14 Otimização: grade espacial (spatial hash)

Com muitos objetos, evite comparar todos com todos (n²):

```
célula = (int(x // TAM), int(y // TAM))
compare apenas objetos da mesma célula e das vizinhas
```

---

## 17. Sprites e Groups

`pygame.sprite.Sprite` é a classe-base para objetos do jogo. Exige `self.image` e `self.rect`.

```python
class Jogador(pygame.sprite.Sprite):
    def __init__(self, pos, *grupos):
        super().__init__(*grupos)                 # já adiciona aos grupos
        self.image = pygame.image.load("player.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.Vector2(self.rect.center)
        self.vel = 300

    def update(self, dt):
        teclas = pygame.key.get_pressed()
        d = pygame.Vector2(teclas[pygame.K_d] - teclas[pygame.K_a],
                           teclas[pygame.K_s] - teclas[pygame.K_w])
        if d: d = d.normalize()
        self.pos += d * self.vel * dt
        self.rect.center = self.pos

todos = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
jogador = Jogador((400, 300), todos)

# loop:
todos.update(dt)       # chama update(dt) em todos
todos.draw(tela)       # desenha image em rect de todos
```

### Métodos de `Sprite`

| Método | Descrição |
|---|---|
| `kill()` | Remove o sprite de **todos** os grupos. |
| `alive()` | `True` se está em algum grupo. |
| `groups()` | Lista de grupos onde está. |
| `add(*grupos)` / `remove(*grupos)` | Adiciona/remove de grupos. |
| `update(*args)` | Você sobrescreve. |

### Métodos de `Group`

| Método | Descrição |
|---|---|
| `add(*sprites)` / `remove(*sprites)` | Gerencia membros. |
| `has(sprite)` | Contém o sprite? |
| `update(*args)` | Chama `update` de cada sprite. |
| `draw(surface)` | Desenha todos (usa `image` e `rect`). |
| `empty()` | Remove todos. |
| `sprites()` | Lista dos sprites. |
| `len(grupo)` | Quantidade. |
| `copy()` | Cópia do grupo. |

### Tipos de Group

| Classe | Uso |
|---|---|
| `Group` | Básico. |
| `GroupSingle` | Guarda **um** sprite só. |
| `LayeredUpdates` | Camadas (z-order): `grupo.add(sprite, layer=2)`. |
| `OrderedUpdates` | Desenha na ordem em que foram adicionados. |
| `LayeredDirty` / `RenderUpdates` | Redesenho parcial (menos usados hoje). |

**Ordenar por profundidade (top-down)**

```python
for s in sorted(todos, key=lambda s: s.rect.bottom):
    tela.blit(s.image, s.rect)
```

### Funções de colisão de sprites

```python
pygame.sprite.spritecollide(sprite, grupo, dokill, collided=None)   # → lista de colididos
pygame.sprite.spritecollideany(sprite, grupo, collided=None)        # → 1º sprite ou None
pygame.sprite.groupcollide(g1, g2, dokill1, dokill2, collided=None) # → {sprite_g1: [sprites_g2]}
```

| Função `collided=` | Teste |
|---|---|
| (padrão) | `rect.colliderect` |
| `pygame.sprite.collide_rect_ratio(0.8)` | Rect reduzido a 80% (hitbox mais justa). |
| `pygame.sprite.collide_circle` | Círculo. Usa `sprite.radius` se existir, senão calcula. |
| `pygame.sprite.collide_circle_ratio(0.8)` | Círculo reduzido. |
| `pygame.sprite.collide_mask` | Pixel perfect (usa `sprite.mask`). |

```python
# Tiros × inimigos: ambos somem
pygame.sprite.groupcollide(tiros, inimigos, True, True)

# Inimigo tocou o jogador?
if pygame.sprite.spritecollide(jogador, inimigos, False, pygame.sprite.collide_circle):
    jogador.vida -= 1

# Coletar moedas
for moeda in pygame.sprite.spritecollide(jogador, moedas, True):
    pontos += 1
```

**Hitbox menor que a imagem**

```python
self.hitbox = self.rect.inflate(-20, -20)     # 10px a menos de cada lado
```

---

## 18. Máscaras (colisão pixel perfect)

Uma `Mask` é um mapa de bits (1 = pixel sólido, 0 = vazio).

```python
mask = pygame.mask.from_surface(imagem)        # a partir dos pixels não transparentes
# (threshold=127: alfa maior que isso conta como sólido)
```

| Método | Descrição |
|---|---|
| `mask.overlap(outra, offset)` | Retorna o 1º ponto de sobreposição `(x, y)` ou `None`. |
| `mask.overlap_area(outra, offset)` | Quantidade de pixels sobrepostos. |
| `mask.overlap_mask(outra, offset)` | Máscara da região sobreposta. |
| `mask.count()` | Total de pixels sólidos. |
| `mask.get_size()` | Tamanho. |
| `mask.get_at((x,y))` / `set_at` | Lê/escreve bit. |
| `mask.outline()` | Lista de pontos do contorno. |
| `mask.centroid()` | Centro de massa. |
| `mask.angle()` | Orientação aproximada. |
| `mask.to_surface()` | Converte p/ Surface (debug). |
| `mask.fill()` / `clear()` / `invert()` | Operações em massa. |

**Fórmula do offset** — posição da *outra* relativa à *minha*:

```
offset = (outro.rect.x - meu.rect.x,  outro.rect.y - meu.rect.y)
```

```python
offset = (b.rect.x - a.rect.x, b.rect.y - a.rect.y)
ponto = a.mask.overlap(b.mask, offset)
if ponto:
    print("Colidiu em", ponto)
```

Com sprites:

```python
self.mask = pygame.mask.from_surface(self.image)
pygame.sprite.collide_mask(a, b)      # retorna ponto ou None
```

> ⚠️ Se a imagem **girar ou mudar de frame**, recrie a máscara. Máscaras são mais pesadas que Rects — use Rect primeiro como filtro e máscara só se o Rect colidir.

---

## 19. Áudio: mixer

```python
pygame.mixer.init()          # normalmente já feito pelo pygame.init()
# Se houver atraso no som: pygame.mixer.pre_init(44100, -16, 2, 512) ANTES do pygame.init()
```

### Efeitos sonoros: `pygame.mixer.Sound`

```python
tiro = pygame.mixer.Sound("assets/tiro.wav")     # .wav e .ogg são os melhores
tiro.set_volume(0.5)                              # 0.0 a 1.0
tiro.play()                                       # play(loops=0, maxtime=0, fade_ms=0)
tiro.play(loops=-1)                               # repete infinitamente
tiro.stop()
tiro.fadeout(500)                                 # some em 500 ms
```

| Método | Descrição |
|---|---|
| `play(loops, maxtime, fade_ms)` | Toca; retorna o `Channel` usado. |
| `stop()`, `fadeout(ms)` | Para. |
| `set_volume(v)`, `get_volume()` | Volume. |
| `get_length()` | Duração em segundos. |
| `get_num_channels()` | Em quantos canais está tocando. |

### Música de fundo: `pygame.mixer.music`

```python
pygame.mixer.music.load("assets/musica.ogg")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=1000)
pygame.mixer.music.pause();  pygame.mixer.music.unpause()
pygame.mixer.music.stop();   pygame.mixer.music.fadeout(1000)
pygame.mixer.music.get_busy()      # está tocando?
pygame.mixer.music.get_pos()       # ms tocados
pygame.mixer.music.queue("proxima.ogg")
pygame.mixer.music.set_endevent(pygame.USEREVENT + 2)   # evento ao terminar
```

> Só **uma** música por vez. Para vários sons simultâneos, use `Sound`.

### Canais

```python
pygame.mixer.set_num_channels(32)         # padrão 8
canal = pygame.mixer.Channel(0)
canal.play(som); canal.set_volume(0.7, 0.3)    # esquerda, direita (pan)
canal = pygame.mixer.find_channel()            # canal livre
```

**Fórmulas**

```
Volume por distância:    vol = clamp(1 - dist / dist_max, 0, 1)
Pan estéreo:             pan = clamp((fonte_x - ouvinte_x) / largura_tela, -1, 1)
                         esquerda = (1 - pan) / 2        direita = (1 + pan) / 2
dB → volume linear:      v = 10 ^ (dB / 20)
```

---

## 20. Tempo, timers e cooldowns

| Função | Descrição |
|---|---|
| `pygame.time.get_ticks()` | ms desde o `pygame.init()`. |
| `pygame.time.wait(ms)` | Pausa (libera CPU; **congela** o jogo). |
| `pygame.time.delay(ms)` | Pausa mais precisa (usa CPU). |
| `pygame.time.set_timer(evento, ms, loops=0)` | Gera um evento a cada `ms` (`0` desliga). |
| `pygame.time.Clock()` | Veja §2. |

### Cooldown (tempo de recarga) sem travar o jogo

```python
COOLDOWN = 300  # ms
ultimo_tiro = 0

agora = pygame.time.get_ticks()
if teclas[pygame.K_SPACE] and agora - ultimo_tiro >= COOLDOWN:
    atirar()
    ultimo_tiro = agora
```

**Fórmula**

```
pode_agir = (agora - ultimo_uso) >= cooldown
tempo_restante = max(0, cooldown - (agora - ultimo_uso))
progresso (0–1) = min(1, (agora - inicio) / duracao)
```

### Timer com dt (compatível com pausa)

```python
timer -= dt
if timer <= 0:
    acao()
    timer = 2.0        # reinicia em 2 s
```

### Cronômetro formatado

```python
segundos = int(tempo_total)
texto = f"{segundos // 60:02d}:{segundos % 60:02d}"
```

### Invencibilidade com piscar

```python
if invencivel:
    visivel = (pygame.time.get_ticks() // 100) % 2 == 0     # alterna a cada 100 ms
```

---

## 21. Animação por frames e spritesheet

### Recortar spritesheet

```python
def carregar_frames(caminho, larg, alt, qtd, escala=1):
    sheet = pygame.image.load(caminho).convert_alpha()
    frames = []
    for i in range(qtd):
        frame = sheet.subsurface((i * larg, 0, larg, alt)).copy()
        if escala != 1:
            frame = pygame.transform.scale(frame, (larg * escala, alt * escala))
        frames.append(frame)
    return frames
```

**Fórmulas (spritesheet em grade)**

```
x = coluna × largura_frame        y = linha × altura_frame
coluna = índice % colunas         linha = índice // colunas
```

### Animação baseada em tempo

```python
class Animacao:
    def __init__(self, frames, fps=10, loop=True):
        self.frames, self.fps, self.loop = frames, fps, loop
        self.tempo = 0.0
        self.indice = 0

    def update(self, dt):
        self.tempo += dt
        total = len(self.frames)
        idx = int(self.tempo * self.fps)
        self.indice = idx % total if self.loop else min(idx, total - 1)

    @property
    def frame(self):
        return self.frames[self.indice]
```

**Fórmula**

```
frame_atual = int(tempo × fps) % total_de_frames
duração_do_ciclo = total_de_frames / fps
```

### Estados de animação

```python
anims = {"parado": anim_parado, "andando": anim_andando, "pulo": anim_pulo}
estado = "andando" if vel.x != 0 else "parado"
if not no_chao: estado = "pulo"
anims[estado].update(dt)
tela.blit(anims[estado].frame, rect)
```

---

## 22. Câmera e scroll

**Ideia:** o mundo é grande; a tela mostra só uma parte. Tudo é desenhado com um **deslocamento (offset)**.

```
posição_na_tela = posição_no_mundo - camera
```

### Câmera que segue o jogador

```python
class Camera:
    def __init__(self, larg_tela, alt_tela, larg_mundo, alt_mundo):
        self.offset = pygame.Vector2()
        self.lt, self.at = larg_tela, alt_tela
        self.lm, self.am = larg_mundo, alt_mundo

    def seguir(self, alvo_rect, dt, suavidade=8):
        desejado = pygame.Vector2(alvo_rect.centerx - self.lt / 2,
                                  alvo_rect.centery - self.at / 2)
        # suaviza (lerp independente de FPS)
        self.offset += (desejado - self.offset) * (1 - math.exp(-suavidade * dt))
        # limita às bordas do mundo
        self.offset.x = max(0, min(self.offset.x, self.lm - self.lt))
        self.offset.y = max(0, min(self.offset.y, self.am - self.at))

    def aplicar(self, rect):
        return rect.move(-self.offset.x, -self.offset.y)

# desenhar:
for s in todos:
    tela.blit(s.image, camera.aplicar(s.rect))
```

**Fórmulas**

```
Centralizar no alvo:      cam = alvo - tamanho_da_tela / 2
Limitar câmera:           cam_x = clamp(cam_x, 0, largura_mundo - largura_tela)
Seguir suavemente:        cam += (alvo - cam) × (1 - e^(-k × dt))
Mouse no mundo:           mundo = mouse + cam
Zoom:                     desenhe o mundo em Surface pequena → transform.scale p/ a tela
                          mundo_x = (tela_x / zoom) + cam_x
Parallax:                 pos_tela = pos_mundo - cam × fator    (fator 0.5 = camada distante)
```

### Fundo que se repete (scroll infinito)

```python
x = -(camera_x * fator) % largura_img
tela.blit(fundo, (x - largura_img, 0))
tela.blit(fundo, (x, 0))
```

---

## 23. Tilemap (mapas de blocos)

```python
TAM = 32
MAPA = [
    "####################",
    "#..................#",
    "#....P.......E.....#",
    "####################",
]

paredes = []
for linha, texto in enumerate(MAPA):
    for coluna, ch in enumerate(texto):
        x, y = coluna * TAM, linha * TAM
        if ch == "#":
            paredes.append(pygame.Rect(x, y, TAM, TAM))
        elif ch == "P":
            jogador_pos = (x, y)
```

**Fórmulas**

```
Mundo → grade:   coluna = x // TAM        linha = y // TAM
Grade → mundo:   x = coluna × TAM         y = linha × TAM
Tamanho do mapa: largura = colunas × TAM  altura = linhas × TAM
Qual tile está sob um ponto:   MAPA[int(y // TAM)][int(x // TAM)]
Isométrico:      tela_x = (col - lin) × larg_tile / 2
                 tela_y = (col + lin) × alt_tile / 2
Iso → grade:     col = (tela_y / (alt/2) + tela_x / (larg/2)) / 2
                 lin = (tela_y / (alt/2) - tela_x / (larg/2)) / 2
```

**Colisão eficiente:** teste apenas os tiles ao redor do jogador:

```python
c0, c1 = int(rect.left // TAM), int(rect.right // TAM)
l0, l1 = int(rect.top // TAM),  int(rect.bottom // TAM)
for l in range(l0, l1 + 1):
    for c in range(c0, c1 + 1):
        if 0 <= l < len(MAPA) and 0 <= c < len(MAPA[0]) and MAPA[l][c] == "#":
            ...  # colisão com o tile (c*TAM, l*TAM, TAM, TAM)
```

> Para mapas feitos no editor **Tiled**, use a biblioteca `pytmx`/`pyscroll`.

---

## 24. Interpolação e easing

**Interpolação linear (lerp)**

```
lerp(a, b, t) = a + (b - a) × t          (t de 0 a 1)
t = tempo_decorrido / duração
```

```python
def lerp(a, b, t): return a + (b - a) * t
```

**Funções de easing (t de 0 a 1)**

```
Linear:        f(t) = t
Ease-in:       f(t) = t²
Ease-out:      f(t) = 1 - (1 - t)²
Ease-in-out:   f(t) = 3t² - 2t³            (smoothstep)
Suave mais:    f(t) = t³(t(6t - 15) + 10)  (smootherstep)
Ease-out cúbico: f(t) = 1 - (1 - t)³
```

```python
def ease_out(t): return 1 - (1 - t) ** 2
def smoothstep(t): return t * t * (3 - 2 * t)

# Exemplo: mover de A até B em 1 segundo
t = min(1, (agora - inicio) / 1000)
pos = a.lerp(b, ease_out(t))
```

**Suavização independente de FPS (para câmera, UI)**

```
valor += (alvo - valor) × (1 - e^(-k × dt))        k maior = mais rápido
```

**Fade in / fade out**

```python
fade = pygame.Surface(tela.get_size())
fade.fill((0, 0, 0))
alpha = int(255 * progresso)       # 0 → 255 (escurece)
fade.set_alpha(alpha)
tela.blit(fade, (0, 0))
```

---

## 25. Interface: botões, barras e texto digitado

### Botão simples

```python
class Botao:
    def __init__(self, rect, texto, fonte, cor=(60,60,60), cor_hover=(90,90,90)):
        self.rect = pygame.Rect(rect)
        self.texto = fonte.render(texto, True, (255,255,255))
        self.cor, self.cor_hover = cor, cor_hover

    def desenhar(self, tela):
        cor = self.cor_hover if self.rect.collidepoint(pygame.mouse.get_pos()) else self.cor
        pygame.draw.rect(tela, cor, self.rect, border_radius=8)
        tela.blit(self.texto, self.texto.get_rect(center=self.rect.center))

    def clicou(self, evento):
        return (evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1
                and self.rect.collidepoint(evento.pos))
```

### Barra de progresso / vida

```python
def barra(tela, x, y, larg, alt, valor, maximo, cor, fundo=(40,40,40)):
    pygame.draw.rect(tela, fundo, (x, y, larg, alt))
    pygame.draw.rect(tela, cor, (x, y, larg * max(0, valor) / maximo, alt))
    pygame.draw.rect(tela, (255,255,255), (x, y, larg, alt), 2)
```

```
largura_preenchida = largura_total × (valor / máximo)
porcentagem = valor / máximo × 100
```

### Campo de texto

```python
texto = ""
for e in pygame.event.get():
    if e.type == pygame.KEYDOWN:
        if e.key == pygame.K_BACKSPACE: texto = texto[:-1]
        elif e.key == pygame.K_RETURN:  enviar(texto)
        else: texto += e.unicode
```

### Slider (0 a 1)

```
valor = clamp((mouse_x - slider.left) / slider.width, 0, 1)
knob_x = slider.left + valor × slider.width
```

### Grade de inventário

```
coluna = índice % colunas        linha = índice // colunas
x = origem_x + coluna × (tamanho + espaço)
y = origem_y + linha  × (tamanho + espaço)
Índice sob o mouse: col = (mx - origem_x) // (tamanho + espaço)
                    lin = (my - origem_y) // (tamanho + espaço)
```

---

## 26. Cenas e estados de jogo

Organize menu, jogo, pausa e game over em **estados**:

```python
class Cena:
    def eventos(self, eventos): pass
    def update(self, dt): pass
    def desenhar(self, tela): pass

class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.cena = Menu(self)
        self.rodando = True

    def trocar_cena(self, nova):
        self.cena = nova

    def run(self):
        while self.rodando:
            dt = self.clock.tick(60) / 1000
            eventos = pygame.event.get()
            for e in eventos:
                if e.type == pygame.QUIT:
                    self.rodando = False
            self.cena.eventos(eventos)
            self.cena.update(dt)
            self.cena.desenhar(self.tela)
            pygame.display.flip()
        pygame.quit()
```

**Pausa simples**

```python
if pausado:
    dt = 0           # ou pule o update()
```

**Máquina de estados do inimigo**

```python
if dist_jogador < 150:   estado = "perseguir"
elif dist_jogador < 300: estado = "alerta"
else:                    estado = "patrulhar"
```

---

## 27. Salvar e carregar dados

```python
import json
from pathlib import Path

SAVE = Path("save.json")

def salvar(dados):
    SAVE.write_text(json.dumps(dados, indent=2), encoding="utf-8")

def carregar():
    if SAVE.exists():
        return json.loads(SAVE.read_text(encoding="utf-8"))
    return {"recorde": 0, "volume": 0.5}

dados = carregar()
dados["recorde"] = max(dados["recorde"], pontos)
salvar(dados)
```

> Para jogos distribuídos, salve em uma pasta do usuário (ex.: `Path.home() / ".meujogo"`), pois a pasta do jogo pode ser somente leitura.

---

## 28. Performance

| Dica | Por quê |
|---|---|
| `convert()` / `convert_alpha()` ao carregar imagens | Blit até 5× mais rápido. |
| Carregue assets **fora** do loop | Ler disco a cada frame trava. |
| Faça cache de textos renderizados | `font.render` é lento. |
| Use `display.flip()` **uma vez** por frame | Evita flicker e desperdício. |
| Use `length_squared()` em vez de `length()` | Evita a raiz quadrada. |
| `blits()` para muitos sprites iguais | Menos chamadas Python. |
| Pré-renderize fundos/tiles estáticos em 1 Surface | 1 blit em vez de milhares. |
| Evite `get_at`/`set_at` em loops | Muito lento; use `PixelArray` ou `surfarray`. |
| Desenhe só o que está na tela | Compare com `tela_rect.colliderect(obj.rect)`. |
| `pygame.SCALED` + resolução baixa | Menos pixels = mais FPS. |
| Mostre o FPS | `f"{clock.get_fps():.0f}"` para detectar gargalos. |
| Perfil | `python -m cProfile -s cumtime jogo.py` |

---

## 29. Empacotar o jogo (.exe)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "assets;assets" main.py     # Windows
pyinstaller --onefile --windowed --add-data "assets:assets" main.py     # Linux/macOS
```

Para achar os assets dentro do executável:

```python
import sys, os

def recurso(caminho):
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, caminho)

img = pygame.image.load(recurso("assets/player.png")).convert_alpha()
```

Alternativa para web: `pygbag` (roda Pygame no navegador).

---

## 30. Erros comuns e boas práticas

| Problema | Causa / Solução |
|---|---|
| Janela "não responde" | Faltou `pygame.event.get()` (ou `event.pump()`) no loop. |
| Tela pisca/rastro | Esqueceu de `tela.fill(...)` a cada frame. |
| Nada aparece | Esqueceu `pygame.display.flip()`/`update()`. |
| `pygame.error: video system not initialized` | Esqueceu `pygame.init()` ou usou depois do `quit()`. |
| Imagem com fundo preto | Use `convert_alpha()` com PNG transparente. |
| Movimento diferente em cada PC | Falta `dt` — use `velocidade × dt`. |
| Personagem treme/anda travado | `Rect` com inteiros: guarde posição real em `float`/`Vector2`. |
| Diagonal mais rápida | Normalize o vetor de direção. |
| Imagem borra ao girar várias vezes | Sempre gire a **original**. |
| Colisão atravessa parede | Mova por eixo, limite velocidade, use `clipline`. |
| Som atrasado | `pygame.mixer.pre_init(44100, -16, 2, 512)` antes de `init()`. |
| Pulo duplo bugado | Use `KEYDOWN` (evento) e `no_chao`, não `get_pressed`. |
| Fonte não achada | Use `Font(None, tamanho)` ou o caminho do `.ttf`. |
| Tela cheia fica distorcida | Use `SCALED` ou calcule a proporção (§3). |
| `pygame` e `pygame-ce` juntos | Desinstale ambos e instale só um. |
| `FileNotFoundError` nos assets | Use `Path(__file__).parent` (§8). |

**Boas práticas**

- Separe **eventos → update → draw**.
- Use constantes em MAIÚSCULAS (`LARGURA`, `FPS`, `GRAVIDADE`) em um arquivo `config.py`.
- Use classes + `Sprite` + `Group`.
- Nunca use `time.sleep()` / `pygame.time.wait()` no loop principal.
- Desenhe um **modo debug** (tecla F3) mostrando hitboxes com `pygame.draw.rect(tela, (255,0,0), rect, 1)`.
- Versione com Git e ignore `__pycache__`.

---

## 31. Cheat sheet de fórmulas

```
── MOVIMENTO ───────────────────────────────────────────────
posição   += velocidade × dt
velocidade += aceleração × dt
dt         = clock.tick(FPS) / 1000
FPS        = 1000 / ms_por_frame

── VETORES ─────────────────────────────────────────────────
comprimento      |v| = √(x² + y²)
normalizar       v / |v|
distância        √((x₂-x₁)² + (y₂-y₁)²)
ângulo           atan2(dy, dx)
direção até alvo (alvo - pos).normalize()
produto escalar  x₁x₂ + y₁y₂
refletir         v - 2(v·n)n
rotacionar       x' = x cosθ - y sinθ   |   y' = x sinθ + y cosθ
graus ↔ rad      rad = graus × π/180

── FÍSICA ──────────────────────────────────────────────────
pulo (v₀)        -√(2 g h)
altura máxima    v₀² / (2g)
tempo p/ o topo  |v₀| / g
projétil         y = y₀ + v₀t + ½ g t²
atrito           v *= (1 - k × dt)
oscilação        y = y₀ + A sin(2π f t)
órbita           (cx + r cos ωt, cy + r sin ωt)

── COLISÃO ─────────────────────────────────────────────────
ponto × rect     left ≤ x < right  e  top ≤ y < bottom
rect × rect      A.left < B.right e A.right > B.left e A.top < B.bottom e A.bottom > B.top
círculo × círc.  dx² + dy² ≤ (r₁ + r₂)²
ponto × círculo  dx² + dy² ≤ r²
círculo × rect   ponto mais próximo = clamp(centro, rect) → compare dist² com r²
sobreposição     min(A.right, B.right) - max(A.left, B.left)
mask offset      (B.x - A.x, B.y - A.y)

── INTERPOLAÇÃO ────────────────────────────────────────────
lerp             a + (b - a) × t
t                tempo_decorrido / duração
ease-out         1 - (1 - t)²
smoothstep       3t² - 2t³
suavizar         v += (alvo - v) × (1 - e^(-k dt))
mapear           a2 + (v - a1)(b2 - a2)/(b1 - a1)
clamp            max(mín, min(v, máx))

── GRADE / TILES ───────────────────────────────────────────
mundo → grade    (x // TAM, y // TAM)
grade → mundo    (col × TAM, lin × TAM)
índice → grade   (i % colunas, i // colunas)

── CÂMERA ──────────────────────────────────────────────────
tela = mundo - camera       mundo = tela + camera
centrar câmera   cam = alvo - tamanho_tela / 2
parallax         pos_tela = pos - cam × fator

── ANIMAÇÃO / TEMPO ────────────────────────────────────────
frame            int(tempo × fps) % n_frames
cooldown         agora - último ≥ intervalo
progresso        (agora - início) / duração
barra de vida    largura × vida / vida_max

── ÁUDIO ───────────────────────────────────────────────────
volume/distância clamp(1 - d / d_max, 0, 1)
pan              clamp((fonte_x - ouvinte_x) / largura, -1, 1)

── TELA ────────────────────────────────────────────────────
centralizar      (tela_w - w) / 2
escala mantendo proporção   min(janela_w / base_w, janela_h / base_h)
```

---

## 32. Template completo de jogo

Cópia e cola para começar um projeto com tudo organizado:

```python
import sys
import math
import random
import pygame
from pygame.math import Vector2

# ---------- CONFIG ----------
LARGURA, ALTURA = 960, 540
FPS = 60
TITULO = "Meu Jogo"

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
FUNDO = (25, 28, 40)


# ---------- ENTIDADES ----------
class Jogador(pygame.sprite.Sprite):
    def __init__(self, pos, *grupos):
        super().__init__(*grupos)
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (80, 200, 120), self.image.get_rect(), border_radius=6)
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(self.rect.center)
        self.vel = 320

    def update(self, dt):
        t = pygame.key.get_pressed()
        d = Vector2(t[pygame.K_d] - t[pygame.K_a], t[pygame.K_s] - t[pygame.K_w])
        if d.length_squared():
            d = d.normalize()
        self.pos += d * self.vel * dt
        self.rect.center = self.pos
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())
        self.pos.update(self.rect.center)


class Moeda(pygame.sprite.Sprite):
    def __init__(self, pos, *grupos):
        super().__init__(*grupos)
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (250, 210, 60), (10, 10), 10)
        self.rect = self.image.get_rect(center=pos)
        self.radius = 10


# ---------- JOGO ----------
class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.SCALED | pygame.RESIZABLE)
        pygame.display.set_caption(TITULO)
        self.clock = pygame.time.Clock()
        self.fonte = pygame.font.Font(None, 32)

        self.todos = pygame.sprite.Group()
        self.moedas = pygame.sprite.Group()
        self.jogador = Jogador((LARGURA // 2, ALTURA // 2), self.todos)
        self.jogador.radius = 20
        self.pontos = 0
        self.debug = False
        self.rodando = True

        for _ in range(10):
            self.criar_moeda()

    def criar_moeda(self):
        pos = (random.randint(30, LARGURA - 30), random.randint(30, ALTURA - 30))
        Moeda(pos, self.todos, self.moedas)

    def eventos(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.rodando = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.rodando = False
                elif e.key == pygame.K_F3:
                    self.debug = not self.debug

    def update(self, dt):
        self.todos.update(dt)
        pegas = pygame.sprite.spritecollide(
            self.jogador, self.moedas, True, pygame.sprite.collide_circle
        )
        for _ in pegas:
            self.pontos += 1
            self.criar_moeda()

    def desenhar(self):
        self.tela.fill(FUNDO)
        self.todos.draw(self.tela)

        txt = self.fonte.render(f"Pontos: {self.pontos}", True, BRANCO)
        self.tela.blit(txt, (12, 10))

        if self.debug:
            fps = self.fonte.render(f"FPS: {self.clock.get_fps():.0f}", True, (255, 255, 0))
            self.tela.blit(fps, (12, 40))
            for s in self.todos:
                pygame.draw.rect(self.tela, (255, 0, 0), s.rect, 1)

        pygame.display.flip()

    def run(self):
        while self.rodando:
            dt = min(self.clock.tick(FPS) / 1000, 0.05)
            self.eventos()
            self.update(dt)
            self.desenhar()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Jogo().run()
```

---

### 📚 Para continuar aprendendo

- Documentação oficial: https://www.pygame.org/docs/
- Pygame Community Edition: https://pyga.me/docs/
- Exemplos prontos: `python -m pygame.examples.<nome>` (ex.: `aliens`, `chimp`, `stars`, `eventlist`)
- Bibliotecas úteis: `pygame_gui` (interface), `pytmx` / `pyscroll` (mapas Tiled), `pymunk` (física 2D avançada), `numpy` (`pygame.surfarray`), `pygbag` (web)

*Manual do Dev Júnior — bom código e bons jogos! 🎮*
