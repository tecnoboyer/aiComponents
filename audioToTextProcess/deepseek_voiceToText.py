from deepseek_api import AudioProcessor, GrammarAnalyzer

# Audio processing
audio_processor = AudioProcessor()
text = audio_processor.transcribe("audio_file.wav")

# Grammatical analysis
grammar_analyzer = GrammarAnalyzer()
analysis = grammar_analyzer.analyze(text)

# Get comprehensive results
print(analysis.get_errors())
print(analysis.get_sentence_structure())