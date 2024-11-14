import 'dart:convert';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  runApp(EnglishLearnApp());
}

class EnglishLearnApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'English Learn App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MainScreen(),
    );
  }
}

class MainScreen extends StatefulWidget {
  @override
  _MainScreenState createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  List<dynamic> words = [];
  String currentWord = '';
  String currentTranslation = '';
  final TextEditingController _controller = TextEditingController();
  List<Map<String, String>> learnedWords = [];
  bool isReviewMode = false;

  @override
  void initState() {
    super.initState();
    loadWords();
  }

  Future<void> loadWords() async {
    final String response = await rootBundle.loadString('assets/words.json');
    final List<dynamic> data = json.decode(response);

    setState(() {
      words = data;
      setRandomWord();
    });

    await loadLearnedWords();
  }

  Future<void> loadLearnedWords() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    List<String>? savedWords = prefs.getStringList('learnedWords') ?? [];

    print('Загруженные слова из SharedPreferences: $savedWords');

    setState(() {
      learnedWords = savedWords
          .where((wordPair) => wordPair.contains(':'))
          .map((wordPair) {
            var splitWords = wordPair.split(':');
            return {'english': splitWords[0], 'russian': splitWords[1]};
          })
          .toList();
    });
  }

  void saveLearnedWord(String english, String russian) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    List<String> savedWords = prefs.getStringList('learnedWords') ?? [];
    String wordPair = '$english:$russian';

    if (!savedWords.contains(wordPair)) {
      savedWords.add(wordPair);
      prefs.setStringList('learnedWords', savedWords);
      print('Сохраненные слова: $savedWords');
      setState(() {
        learnedWords.add({'english': english, 'russian': russian});
      });
    }
  }

  void incrementCounter(String englishWord, bool isCorrect, bool isReviewMode) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String key = '${englishWord}_stats';
    
    List<String> counters = prefs.getStringList(key) ?? ['0', '0', '0', '0'];
    
    int correctRegular = int.parse(counters[0]);
    int correctReview = int.parse(counters[1]);
    int errorsRegular = int.parse(counters[2]);
    int errorsReview = int.parse(counters[3]);
    
    if (isCorrect) {
      if (isReviewMode) {
        correctReview++;
      } else {
        correctRegular++;
      }
    } else {
      if (isReviewMode) {
        errorsReview++;
      } else {
        errorsRegular++;
      }
    }
    
    prefs.setStringList(key, [
      correctRegular.toString(),
      correctReview.toString(),
      errorsRegular.toString(),
      errorsReview.toString(),
    ]);

    setState(() {}); // обновляем экран
  }

  void setRandomWord() {
    if (words.isNotEmpty) {
      final randomIndex = Random().nextInt(words.length);
      currentWord = words[randomIndex]['translation'];
      currentTranslation = words[randomIndex]['word'];
    }
  }

  void checkAnswer() {
  String userInput = _controller.text.trim().toLowerCase(); // Приводим пользовательский ввод к нижнему регистру
  String correctWord = currentTranslation.trim().toLowerCase(); // Сравниваем с правильным английским словом

  print('Пользовательский ввод: "$userInput"');
  print('Правильный ответ: "$correctWord"');

  bool isCorrect = userInput == correctWord; // Проверка на равенство

  incrementCounter(currentTranslation, isCorrect, isReviewMode);

  if (isCorrect) {
    saveLearnedWord(currentTranslation, currentWord);
    setState(() {
      setRandomWord();
      _controller.clear();
    });
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Правильно! Новое слово загружено.')),
    );
  } else {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Неверно, попробуйте снова.')),
    );
  }
}

  Future<List<String>> getCounters(String englishWord) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    return prefs.getStringList('${englishWord}_stats') ?? ['0', '0', '0', '0'];
  }

  void openReviewMode() {
    setState(() {
      isReviewMode = true;
      setRandomWord();
    });
  }

  void returnToMainMenu() {
    setState(() {
      isReviewMode = false;
      setRandomWord();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("English Learn"),
        backgroundColor: const Color.fromARGB(255, 95, 178, 247),
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            Container(
              height: 220, // Увеличиваем высоту DrawerHeader
              child: DrawerHeader(
                decoration: BoxDecoration(
                  color: const Color.fromARGB(255, 95, 178, 247),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Словарь выученных слов',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 22,
                      ),
                    ),
                    SizedBox(height: 10),
                    Text(
                      'Зелёный: правильные (обычный)',
                      style: TextStyle(
                        color: Colors.green,
                        fontSize: 14,
                      ),
                    ),
                    Text(
                      'Синий: правильные (проверка)',
                      style: TextStyle(
                        color: Colors.blue,
                        fontSize: 14,
                      ),
                    ),
                    Text(
                      'Красный: ошибки (обычный)',
                      style: TextStyle(
                        color: Colors.red,
                        fontSize: 14,
                      ),
                    ),
                    Text(
                      'Оранжевый: ошибки (проверка)',
                      style: TextStyle(
                        color: Colors.orange,
                        fontSize: 14,
                      ),
                    ),
                  ],
                ),
              ),
            ),
            SingleChildScrollView(
              child: Column(
                children: learnedWords.map((wordPair) {
                  String english = wordPair['english'] ?? '';
                  String russian = wordPair['russian'] ?? '';
                  return FutureBuilder<List<String>>(
                    future: getCounters(english),
                    builder: (context, snapshot) {
                      if (!snapshot.hasData) return Container();
                      List<String> counters = snapshot.data!;
                      return ListTile(
                        title: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(english), // Английское слово
                            SizedBox(height: 4), // Небольшой отступ
                            Text(
                              russian.isEmpty ? 'Перевод не найден' : russian,
                              style: TextStyle(color: Colors.grey),
                            ), // Русское слово
                          ],
                        ),
                        trailing: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Text(counters[0], style: TextStyle(color: Colors.green)),
                            SizedBox(width: 4),
                            Text(counters[1], style: TextStyle(color: Colors.blue)),
                            SizedBox(width: 4),
                            Text(counters[2], style: TextStyle(color: Colors.red)),
                            SizedBox(width: 4),
                            Text(counters[3], style: TextStyle(color: Colors.orange)),
                          ],
                        ),
                      );
                    },
                  );
                }).toList(),
              ),
            ),
          ],
        ),
      ),
      body: Stack(
        children: [
          Image.asset(
            'assets/background.jpg',
            fit: BoxFit.cover,
            width: double.infinity,
            height: double.infinity,
          ),
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  isReviewMode
                      ? 'Введите перевод для: $currentTranslation'
                      : 'Введите перевод для: $currentWord',
                  style: TextStyle(fontSize: 20),
                ),
                SizedBox(height: 10),
                TextField(
                  controller: _controller,
                  decoration: InputDecoration(
                    border: OutlineInputBorder(),
                    labelText: 'Перевод',
                  ),
                ),
                SizedBox(height: 10),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    ElevatedButton(
                      onPressed: checkAnswer,
                      child: Text(isReviewMode ? 'Проверить' : 'Ответить'),
                    ),
                    SizedBox(width: 10),
                    ElevatedButton(
                      onPressed: isReviewMode ? returnToMainMenu : openReviewMode,
                      child: Text(isReviewMode ? 'Главное меню' : 'Режим проверки'),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
