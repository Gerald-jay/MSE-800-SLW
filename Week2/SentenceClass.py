class sentenceClass:
    def set_sentence(self,sentence):
        self.sentence = sentence

    def count_words(self):
        words = self.sentence
        return len(words)
    
    def input_sentence(self):
        sentence = input("Please input your setence:")
        if not sentence.strip():
            print("You entered an empty sentence.")
            self.input_sentence()
            
        return sentence

if __name__ == "__main__":
    analyzer = sentenceClass()
    analyzer.set_sentence(analyzer.input_sentence())
    print("Word count:", analyzer.count_words())

