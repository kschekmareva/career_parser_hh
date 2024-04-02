import csv
import time
from main import Browser

br = Browser()

analyst_levels = ['junior', 'middle', 'senior', 'other']
analyst_lists = {level: [] for level in analyst_levels}
analyst_counts = {level: 0 for level in analyst_levels}


def write_to_csv():
    for i in range(10):
        for elem in br.parse():
            for el in analyst_levels:
                if el in elem.text.lower():
                    analyst_lists[el].append(elem.get_text('; '))
                    analyst_counts[el] += 1
                else:
                    analyst_lists['other'].append(elem.get_text('; '))
                    analyst_counts['other'] += 1

        print('Writing to CSV files...')
        for level in analyst_levels:
            with open(f'{level}_analysts.csv', 'a', encoding='utf-8') as file:
                write_to_csv_ = csv.writer(file)
                for row in analyst_lists[level]:
                    write_to_csv_.writerow([row])

            analyst_lists[level].clear()

        print('СЛЕДУЮЩАЯ СТРАНИЦА!')
        br.to_next_page(i + 2)
        time.sleep(3)


posts = ['Аналитика Данных', 'Data Science']
for idx, post in enumerate(posts):
    if idx == 0:
        br.search(post)
        write_to_csv()
    elif 1 <= idx < (len(posts) - 1):
        br.clear_search(post)
        write_to_csv()
    else:
        br.clear_search(post)
        write_to_csv()
        br.exit()

with open('analyst_counts.csv', 'w', encoding='utf-8') as counts_file:
    writer = csv.writer(counts_file)
    writer.writerow(['Level', 'Count'])
    for level, count in analyst_counts.items():
        writer.writerow([level.capitalize(), count])