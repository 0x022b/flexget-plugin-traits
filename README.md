# FlexGet Traits

Traits is a FlexGet plugin that will replace one or more of internal quality
requirement types with new ones defined in a configuration file.

## Usage

### Installation

To install `traits` copy its Python file into FlexGet's `plugins` directory that
is usually located in `${HOME}/.config/flexget/`. Create the directory if it doesn't
already exist. The included example configuration file is not needed but it can be
used either as is or as a starting point for a custom configuration.

```
${HOME}/.config/flexget/
├── plugins
│   └── traits.py
└── traits.yaml
```

### Example

This configuration example assumes that the included `traits.yaml` file is being
used as described above. Here the `premieres` task is configured to use `traits`
and `series_premiere` plugins to accept entries that have `1080p` resolution and
`eac3` audio.

```yaml
---
tasks:
  premieres:
    include:
      - traits.yaml
    series_premiere:
      quality: 1080p eac3
```

### Schema

Plugin uses the following schema for its configuration.

```json
{
    "type": "object",
    "properties": {
        "audio": { "$ref": "#/$defs/qualities" },
        "codec": { "$ref": "#/$defs/qualities" },
        "color_range": { "$ref": "#/$defs/qualities" },
        "resolution": { "$ref": "#/$defs/qualities" },
        "source": { "$ref": "#/$defs/qualities" },
    },
    "additionalProperties": false,
    "$defs": {
        "qualities": {
            "type": "object",
            "minProperties": 1,
            "additionalProperties": {
                "type": "object",
                "properties": {
                    "value": { "type": "integer" },
                    "regexp": { "type": "string" },
                    "modifier": { "type": "integer" },
                    "defaults": { "type": "array" },
                },
                "required": ["value"],
                "additionalProperties": false,
            },
        },
    },
}
```

## Quality requirements

The included `traits.yaml` configuration example supports the following quality
requirements which are a little bit different from what FlexGet natively supports.
Qualities are in general weighted so that they are preferred in the following order:
source, resolution, audio, colour range and codec. The order is also somewhat different
compared to built-in qualities and should more precisely sort them by quality.

Qualities included in the example configuration are listed below from best to worst.

### Source

Identifier  | Description
------------|------------
bluray      | Remuxed or transcoded directly from a Blu-ray disc.
webdl       | Losslessly ripped from a streaming service.
webrip      | Extracted using the HLS or RTMP/E protocols and remuxed from a TS, MP4 or FLV container to MKV.
hdrip       | Typically transcoded versions of HDTV or WEB-DL source files, but may be any type of HD transcode.
webcap      | Captured from a DRM-enabled streaming service.
hchdrip     | Captured from a DRM-enabled streaming service with hard-coded subtitles.
vodrip      | Recorded or captured from an On-Demand service such as through a cable or satellite TV service.
tvrip       | Recorder or captured from any television source.
dvd         | Final retail version of a film in DVD format, generally a complete copy from the original DVD.
dvdrip      | Transcoded final retail version of a film from the original DVD.
r5          | Studio produced unmastered telecine put out quickly and cheaply to compete against telecine piracy.
ddc         | Digital distribution copy is basically the same as a screener, but sent digitally (FTP, HTTP, etc.) to companies instead of via the postal system.
screener    | Early DVD or BD releases of the theatrical version of a film.
ppvrip      | Recorded or captured from a Pay-Per-View source.
telecine    | Captured from a film print using a machine that transfers the movie from its analog reel to digital format.
workprint   | Copy made from an unfinished version of a film produced by the studio.
telesync    | Bootleg recording of a film recorded in a movie theater.
cam         | Copy made in a cinema using a camcorder or mobile phone.

More detailed descriptions for each identifier are available from Wikipedia article
[Pirated_movie_release_types](https://en.wikipedia.org/wiki/Pirated_movie_release_types).

### Audio

Identifier  | Description
------------|------------
dtshd       | [DTS-HD Master Audio](https://en.wikipedia.org/wiki/DTS-HD_Master_Audio)
truehd      | [Dolby TrueHD](https://en.wikipedia.org/wiki/Dolby_TrueHD)
flac        | [FLAC](https://en.wikipedia.org/wiki/FLAC)
eac3        | [Dolby Digital Plus](https://en.wikipedia.org/wiki/Dolby_Digital_Plus)
dts         | [DTS](https://en.wikipedia.org/wiki/DTS_(sound_system))
ac3         | [Dolby Digital](https://en.wikipedia.org/wiki/Dolby_Digital)
aac         | [AAC](https://en.wikipedia.org/wiki/Advanced_Audio_Coding)
mp3         | [MP3](https://en.wikipedia.org/wiki/MP3)

### Codec

Identifier  | Description
------------|------------
av1         | [AV1](https://en.wikipedia.org/wiki/AV1)
h265        | [H.265](https://en.wikipedia.org/wiki/High_Efficiency_Video_Coding)
vp9         | [VP9](https://en.wikipedia.org/wiki/VP9)
h264        | [H.264](https://en.wikipedia.org/wiki/Advanced_Video_Coding)
vc1         | [VC-1](https://en.wikipedia.org/wiki/VC-1)
xvid        | [Xvid](https://en.wikipedia.org/wiki/Xvid)
divx        | [DivX](https://en.wikipedia.org/wiki/DivX)

### Color Range

Identifier  | Description
------------|------------
dolbyvision | [Dolby Vision](https://en.wikipedia.org/wiki/Dolby_Vision)
hdrplus     | [HDR10+](https://en.wikipedia.org/wiki/HDR10%2B)
hdr         | [HDR10](https://en.wikipedia.org/wiki/HDR10)
10bit       | [High 10 Profile](https://en.wikipedia.org/wiki/Advanced_Video_Coding#Profiles) / [Main 10 Profile](https://en.wikipedia.org/wiki/High_Efficiency_Video_Coding#Main_10)

If no color range is defined, 8 bit color depth is implied.

### Resolution

Identifier  | Description
------------|------------
2160p       | [2160p](https://en.wikipedia.org/wiki/4K_resolution#2160p_resolution)
1440p       | [1440p](https://en.wikipedia.org/wiki/1440p)
1080p       | [1080p](https://en.wikipedia.org/wiki/1080p)
1080i       | [1080i](https://en.wikipedia.org/wiki/1080i)
720p        | [720p](https://en.wikipedia.org/wiki/720p)
576p        | [576p](https://en.wikipedia.org/wiki/576p)
576i        | [576i](https://en.wikipedia.org/wiki/576i)
480p        | [480p](https://en.wikipedia.org/wiki/480p)
360p        | [360p](https://en.wikipedia.org/wiki/Low-definition_television)

## Development

This project is built using [Poetry][poetry] packaging and dependency management tool.

### Install dependencies

To install project dependencies in a virtual environment run the following command:

```shell
poetry install
```

### Code formatting

[The Black code style][black] is used throughout the project. To format all code
in the project using the Black code style execute the following command:

```shell
poetry run black .
```

### Unit tests

Unit tests for this project are written using [pytest][pytest]. To run all tests
execute the following command:

```shell
poetry run pytest
```

## License

MIT

[black]: https://black.readthedocs.io/en/stable/the_black_code_style/index.html
[poetry]: https://python-poetry.org/
[pytest]: https://pytest.org/
