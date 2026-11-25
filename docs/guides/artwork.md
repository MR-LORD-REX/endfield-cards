# Custom artwork

Character and Compare cards accept optional artwork. Without it, the card uses the character art supplied by skport-py.

```python
from pathlib import Path
from endfield_cards import Artwork

result = await cards.character_card(
    skport_id,
    name="Zhuang Fangyi",
    template=1,
    art=Artwork(Path("art/operator.png"), fit="cover", focal_point=(0.5, 0.3)),
)
```

`art` also accepts a local path, image bytes, or a Pillow image directly. `Artwork` gives you explicit crop controls:

- `fit="cover"` fills the artwork frame and crops excess edges.
- `fit="contain"` keeps the complete image inside the frame.
- `focal_point=(x, y)` places the crop focus using normalized coordinates from 0 to 1.
- `allow_remote=True` enables an HTTP(S) source.
- `retain=True` requests retention under the renderer's cache policy.

Input images are copied before processing; your original Pillow pixels remain unchanged.

## Remote artwork

Enable remote loading explicitly:

```python
art = Artwork("https://example.com/operator.png", allow_remote=True)
result = await cards.character_card(skport_id, index=0, art=art)
```

The renderer applies its download and decoded-image limits. Use images you have permission to publish.

## Comparison artwork

`art` controls the first player's artwork; `second_art` controls the second:

```python
result = await cards.compare_card(
    first_skport_id,
    second_skport_id,
    name="Zhuang Fangyi",
    art=Artwork(Path("art/first.png")),
    second_art=Artwork(Path("art/second.png")),
)
```
