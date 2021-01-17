import json
import logging

logger = logging.getLogger(__name__)

OG_PICK_STRING = '______'
FINAL_PICK_STRING = '_'


def normalize_text(text):
    return text.replace(OG_PICK_STRING, FINAL_PICK_STRING).replace("\"", "\'")


def normalize_newline(text):
    return [line.replace("\\n", "\n") for line in text]


def read_file(filename):
    file_content = []
    with open(filename, encoding="utf8") as file:
        content = normalize_text(file.read())
        content_list = normalize_newline(content.splitlines())
        file_content.extend(content_list)

    return file_content


def compute_black_card(text):
    pick = int(text.count(FINAL_PICK_STRING))
    return {'text': text, 'pick': pick if pick != 0 else 1}


def generate_black_cards_json(cards, output_json):
    for text in cards:
        black_card = compute_black_card(text)
        output_json['black'].append(black_card)


def write_file(filename, json_data):
    with open(filename, 'w', encoding="utf8") as file:
        file.write(json.dumps(json_data, ensure_ascii=False))


def main():
    logger.info('Reading white and black cards files')
    white_cards_text = read_file('white.txt')
    white_cards_count = len(white_cards_text)
    black_cards_text = read_file('black.txt')
    black_cards_count = len(black_cards_text)
    white_black_dict = {'white': [], 'black': []}

    logger.info('Generating black cards final json structure')
    generate_black_cards_json(black_cards_text, white_black_dict)
    white_black_dict['white'] = white_cards_text
    white_black_dict['packs'] = {
        'base': {
            "name": "The Base Set",
            "description": "Sweet dirty vanilla",
            "official": False,
            "white": [i for i in range(0, white_cards_count)],
            "black": [i for i in range(0, black_cards_count)],
        }
    }

    logger.info('Writing data into output.json')
    write_file('output.json', white_black_dict)

    return 0


if __name__ == "__main__":
    main()
