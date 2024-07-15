# GetVM Playground Icons

This repository contains the icons used in the GetVM Playground. Over 400+ programming language icons, providing SVG and PNG formats.

[![](https://data.jsdelivr.com/v1/package/gh/getvmio/getvm-icons/badge)](https://www.jsdelivr.com/package/gh/getvmio/getvm-icons)

## Usage

All raw SVG files are in the `logos` folder. The masked icons are in the `icons` folder.

You can use the icons by accessing the [JSdelivr CDN](https://www.jsdelivr.com/package/gh/getvmio/getvm-icons), e.g.: <https://cdn.jsdelivr.net/gh/getvmio/getvm-icons@main/icons/linux.png>

| Logo | Raw SVG | Masked PNG |
| --- | --- | --- |
| Linux | <img src="https://cdn.jsdelivr.net/gh/getvmio/getvm-icons/logos/linux.svg" width="64" height="64"> | <img src="https://cdn.jsdelivr.net/gh/getvmio/getvm-icons/icons/linux.png" width="64" height="64">

## Adding New Icons

1. Add logos to the `logos` folder.
2. Run `mask.py` to generate masked logos, which will be saved in the `icons` folder.
3. Commit and push the changes, then create a pull request, and we will review it.
4. Once the pull request is merged, the new icons will be available on the [CDN](https://www.jsdelivr.com/package/gh/getvmio/getvm-icons).

## License

Raw icons are from Internet sources and are licensed under their respective licenses. The masked icons are licensed under the MIT License.
