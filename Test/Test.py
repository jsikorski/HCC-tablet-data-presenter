from loaderHTD import DataHTD

htd = DataHTD("1.htd")

print htd.header
for package in htd.packages:
    print package[4]
