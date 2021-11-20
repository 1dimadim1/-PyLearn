seconds = int(1000000)
minutes = seconds // 60
hours = minutes // 60
days = hours // 24
print(f"{days} дней, {hours % 24} часов, {minutes % 60} минут, {seconds % 60} секунд")