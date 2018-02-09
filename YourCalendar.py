try:
    import sys
    import argparse
    import os
    from PIL import Image, ImageDraw, ImageFont
except Exception as exc:
    print('Game modules not found: "{}"'.format(exc), file=sys.stderr)
    sys.exit(1)


class Painter:
    def __init__(self, width_calendar, height_calendar):
        self.img = Image.new('RGB', (width_calendar, height_calendar), 'white')
        self.row = 6
        self.column = 7
        self.width_side = width_calendar // self.column
        self.height_side = height_calendar // self.row

    def paint(self, days, days_x, name_month, title, path):
        week = 0
        center_cell = self.width_side // 2 - self.width_side // 3
        top = 10
        drawer = ImageDraw.Draw(self.img)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 14)
            font_for_title = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 18)
        except Exception as e:
            try:
                font = ImageFont.truetype("arial.ttf", 12)
                font_for_title = font = ImageFont.truetype("arial.ttf", 16)
            except Exception as exc:
                print("Failed to find the font")
                sys.exit(1)
        for i in range(0, len(days)):
            width = (days[i] - 1) * self.width_side
            height = week * self.height_side
            bacground = 'white'
            if days[i] in [6, 7]:
                bacground = 'red'
            drawer.rectangle([width, height, width + self.width_side, height + self.height_side], bacground, 'black')
            drawer.text((width + center_cell, height + top), name_month + ' ' + str(i + 1),   fill='black', font=font)
            if i+1 in days_x:
                drawer.text((width + center_cell, height + self.height_side // 2), title, fill='black',
                            font=font_for_title)
            if days[i] == 7:
                week += 1
        self.img.save(path)


class Algorithm:

    def main(self, day_of_week, numbder_days_month):
        days = [i for i in range(1, numbder_days_month + 1)]
        gone = 7 - day_of_week + 1
        if day_of_week > 7 or day_of_week < 1:
            print('Sorry but in the week of 7 days')
            return
        data = []
        for day in days:
            result = (day - gone) % 7
            if result == 0:
                result = 7
            data.append(result)
        return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('day', help='day of the week from which the month begins', type=int)
    parser.add_argument('month', help='name of month')
    parser.add_argument('--title', help='inscription on selected days', default='You can')
    parser.add_argument('--path', help='path to picture', default=os.path.join(os.getcwd(), "result.png"))
    parser.add_argument('--count', help="number of days in a month", type=int, default=31)
    parser.add_argument('--width', help='width of image', type=int, default=800)
    parser.add_argument('--height', help='height of image', type=int, default=600)
    print('Enter the dates you require')
    args = parser.parse_args()
    dates = input().split(' ')
    acceptable_date = []
    for date in dates:
        try:
            acceptable_date.append(int(date))
        except Exception as e:
            continue
    alg = Algorithm()
    painter = Painter(args.width, args.height)
    painter.paint(alg.main(args.day, args.count), acceptable_date, args.month, args.title, args.path)

