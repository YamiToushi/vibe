class Repo {
  final int id;
  final String name;
  final String? description;
  final String htmlUrl;
  final DateTime createdAt;
  final DateTime updatedAt;
  final String? language;
  final int stars;
  final int forks;
  final bool isFork;
  final List<String> topics;

  const Repo({
    required this.id,
    required this.name,
    this.description,
    required this.htmlUrl,
    required this.createdAt,
    required this.updatedAt,
    this.language,
    required this.stars,
    required this.forks,
    required this.isFork,
    required this.topics,
  });

  factory Repo.fromJson(Map<String, dynamic> j) => Repo(
        id: j['id'] as int,
        name: j['name'] as String,
        description: j['description'] as String?,
        htmlUrl: j['html_url'] as String,
        createdAt: DateTime.parse(j['created_at'] as String),
        updatedAt: DateTime.parse(j['updated_at'] as String),
        language: j['language'] as String?,
        stars: j['stargazers_count'] as int,
        forks: j['forks_count'] as int,
        isFork: j['fork'] as bool,
        topics:
            (j['topics'] as List?)?.map((e) => e as String).toList() ?? [],
      );
}
