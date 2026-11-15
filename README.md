<div align="center">
    <img src="Animations/gameplay.gif" width="600"/>
</div>
<br/>

> 🇧🇷 [Português](#o-que-você-encontrará-neste-repositório) · 🇺🇸 [English](#what-will-you-find-in-this-repository)

## O que você encontrará neste repositório?

Protótipo construído para a [One Button Game Jam](https://itch.io/jam/one-button-game) de junho de 2020. Minha primeira
participação em uma Game Jam e a primeira tentativa de jogo autoral (o que não foi uma boa ideia).

Cat-n-shoot é um shooter de plataforma com uma estética não uniforme, mas agradável. A base do movimento do jogo vem dos
jogos e tutoriais do [DaFluffyPotato](https://www.youtube.com/c/DaFluffyPotato), o desenvolvedor central da comunidade
Pygame. Alguns sprites e áudios são autorais, enquanto outros são de mídia free-to-use.

Infelizmente, o prazo não foi cumprido. Entretanto, o resultado é funcional e bonito.

### Ferramentas

* Python 3
* [Pygame](https://www.pygame.org/) (gráficos, física, áudio e entrada)

### Como jogar

Fiel à proposta da jam, o jogo usa **um único botão**: tudo é controlado pela posição do mouse e pelo clique.

| Mouse                                  | Ação                                                    |
|----------------------------------------|---------------------------------------------------------|
| Terço direito / esquerdo da tela       | Andar (e correr, depois de um tempo andando)            |
| Faixa logo abaixo do topo da tela      | Pular (o topo em si é neutro: o gato fica parado)       |
| Parte inferior da tela                 | Carregar o super pulo de foguete (recarrega em 8 s)     |
| Clique esquerdo (segurar)              | Atirar (15 tiros, depois 2 s para recarregar)           |

As setas na tela acendem para mostrar a ação ativa. Cair por muito tempo encerra o jogo.

### Como usar

```bash
git clone https://github.com/tofolo17/cat-n-shoot.git
cd cat-n-shoot
pip install -r requirements.txt
python main.py
```

O mapa fica em `mapfile.txt`: cada caractere é um bloco (`0` = vazio), então dá para editar a fase num editor de texto.

### Licença

[MIT](LICENSE)

---

## What will you find in this repository?

Prototype built for the [One Button Game Jam](https://itch.io/jam/one-button-game) from June 2020. My first
participation in a Game Jam and the first attempt at an authorial game (what was not a good combo).

Cat-n-shoot is a platform shooter with a non-uniform but pleasant aesthetic. The foundation of the game's movement comes
from games and tutorials by [DaFluffyPotato](https://www.youtube.com/c/DaFluffyPotato), the core developer of the Pygame
community. A few sprites and audios are authorial, while others are from free-to-use media.

Unfortunately, the deadline was not met. However, the result is functional and beautiful.

### Tools

* Python 3
* [Pygame](https://www.pygame.org/) (graphics, physics, audio and input)

### How to play

True to the jam's theme, the game uses **a single button**: everything is controlled by the mouse position and click.

| Mouse                                  | Action                                                  |
|----------------------------------------|---------------------------------------------------------|
| Right / left third of the screen       | Walk (and run, after walking for a while)               |
| Band just below the top of the screen  | Jump (the very top is neutral: the cat stands still)    |
| Bottom of the screen                   | Charge the rocket super jump (recharges in 8 s)         |
| Left click (hold)                      | Shoot (15 shots, then 2 s to reload)                    |

On-screen arrows light up to show the active action. Falling for too long ends the game.

### How to use

```bash
git clone https://github.com/tofolo17/cat-n-shoot.git
cd cat-n-shoot
pip install -r requirements.txt
python main.py
```

The map lives in `mapfile.txt`: each character is a tile (`0` = empty), so you can edit the level in a text editor.

### License

[MIT](LICENSE)
