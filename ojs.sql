SELECT CONCAT('/home/garnett/insap/bd/journals/', articles.journal_id,'/articles/', articles.article_id, '/public/', article_files.file_name), 
	issues.volume, 
	issues.number, 
	issues.year, 
	journal_settings.setting_value as journal_title, 
	arttitle.setting_value as article_title, 
	artabstract.setting_value as article_abstract, 
	GROUP_CONCAT(concat(authors.last_name, ',', authors.first_name, ' ', authors.middle_name) SEPARATOR ';') as author_name, 
	GROUP_CONCAT(authors.email SEPARATOR ';') as author_email, 
	GROUP_CONCAT(authors.primary_contact SEPARATOR ';'), 
	GROUP_CONCAT(authaffiliation.setting_value SEPARATOR ';') as author_affiliation
FROM article_files
	JOIN articles ON article_files.article_id = articles.article_id
	JOIN journal_settings ON articles.journal_id = journal_settings.journal_id
	JOIN published_articles ON published_articles.article_id = articles.article_id
	JOIN issues ON issues.issue_id = published_articles.issue_id
	JOIN article_settings arttitle ON arttitle.article_id = articles.article_id
	JOIN article_settings artabstract ON artabstract.article_id = articles.article_id
	JOIN authors ON authors.submission_id = articles.article_id
	JOIN author_settings authaffiliation ON authors.author_id = authaffiliation.author_id
WHERE journal_settings.setting_name="title" 
	AND article_files.type="public" 
	AND authaffiliation.setting_name="affiliation" 
	AND arttitle.setting_name = 'title' 
	AND artabstract.setting_name = 'abstract'
GROUP BY 1, 2, 3, 4, 5, 6, 7