from core.ansicolors import AnsiColors

def print_logo() -> None:
  """Print the GV Robot Pi logo"""
  logo = open("./logo.txt", "r")
  print(AnsiColors.OKBLUE + AnsiColors.BOLD + logo.read() + AnsiColors.ENDC + "\n")
  logo.close()