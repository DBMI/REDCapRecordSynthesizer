cd C:\\Users\\Kevin.Delaney\\PycharmProjects\\RecordSynthesizer
coverage run -m unittest discover
coverage xml
genbadge coverage --input-file coverage.xml --output-file .\\.github\\badges\\coverage-badge.svg