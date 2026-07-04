CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `avatar_url` varchar(255) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `is_vip` tinyint(1) NOT NULL DEFAULT '0',
  `vip_expire_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `courses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `description` text,
  `cover_url` varchar(255) DEFAULT NULL,
  `difficulty` enum('beginner','intermediate','advanced') NOT NULL,
  `duration_seconds` int NOT NULL,
  `category` varchar(50) NOT NULL,
  `status` varchar(50) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `course_sections` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course_id` int NOT NULL,
  `title` varchar(100) NOT NULL,
  `content_english` text,
  `content_chinese` text,
  `audio_url` varchar(255) DEFAULT NULL,
  `video_url` varchar(255) DEFAULT NULL,
  `sort_order` int NOT NULL,
  `duration_seconds` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `course_sections_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `membership_plans` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `price_cents` int NOT NULL,
  `duration_days` int NOT NULL,
  `description` text,
  `features_json` json NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `user_memberships` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `plan_id` int NOT NULL,
  `start_date` datetime NOT NULL,
  `end_date` datetime NOT NULL,
  `status` varchar(50) NOT NULL,
  `payment_method` varchar(50) DEFAULT NULL,
  `transaction_id` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `plan_id` (`plan_id`),
  CONSTRAINT `user_memberships_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `user_memberships_ibfk_2` FOREIGN KEY (`plan_id`) REFERENCES `membership_plans` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `study_records` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `course_id` int NOT NULL,
  `section_id` int DEFAULT NULL,
  `study_date` datetime NOT NULL,
  `review_count` int NOT NULL DEFAULT '0',
  `ease_factor` decimal(3,1) NOT NULL DEFAULT '2.5',
  `interval_days` int NOT NULL DEFAULT '4',
  `next_review_at` datetime,
  `status` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `course_id` (`course_id`),
  KEY `section_id` (`section_id`),
  CONSTRAINT `study_records_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `study_records_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`),
  CONSTRAINT `study_records_ibfk_3` FOREIGN KEY (`section_id`) REFERENCES `course_sections` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `listening_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `course_id` int NOT NULL,
  `duration_listened` int NOT NULL,
  `comprehension_score` decimal(3,1) NOT NULL,
  `completed_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `listening_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `listening_logs_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `payments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `amount_cents` int NOT NULL,
  `payment_method` varchar(50) NOT NULL,
  `transaction_id` varchar(100) NOT NULL,
  `status` varchar(50) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 插入测试数据
INSERT INTO `users` (`username`, `password_hash`, `email`, `created_at`, `updated_at`) VALUES
('teacher1', '$2b$12$YCtSjkhD9kdf23EhggsznOMlD3S8zvxP1cTmQyqTF3s2SDXFGKO6.', 'teacher1@woxueshe.com', NOW(), NOW()),
('student1', '$2b$12$YCtSjkhD9kdf23EhggsznOMlD3S8zvxP1cTmQyqTF3s2SDXFGKO6.', 'student1@woxueshe.com', NOW(), NOW()),
('student2', '$2b$12$YCtSjkhD9kdf23EhggsznOMlD3S8zvxP1cTmQyqTF3s2SDXFGKO6.', 'student2@woxueshe.com', NOW(), NOW());

INSERT INTO `courses` (`title`, `description`, `cover_url`, `difficulty`, `duration_seconds`, `category`, `status`, `created_at`) VALUES
('考研英语核心词汇', '精选1000个考研英语高频词汇，搭配语境例句', 'cover_kaoyan.jpg', 'advanced', 7200, '考研英语', 'active', NOW()),
('四六级听力突破', '听力专项训练，涵盖历年真题对话与讲座', 'cover_cet46.jpg', 'intermediate', 5400, '四六级', 'active', NOW()),
('托福口语入门', '从基础发音到流利表达，适合托福初学者', 'cover_toefl.jpg', 'beginner', 3600, '托福', 'active', NOW()),
('雅思写作模板', '大作文小作文模板与高分句式分析', 'cover_ielts.jpg', 'intermediate', 9000, '雅思', 'active', NOW()),
('日常英语会话', '覆盖点餐、问路、购物等真实场景', 'cover_daily.jpg', 'beginner', 4800, '日常口语', 'active', NOW());

INSERT INTO `course_sections` (`course_id`, `title`, `content_english`, `content_chinese`, `audio_url`, `video_url`, `sort_order`, `duration_seconds`) VALUES
(1, '词根词缀法', 'Understanding root words and affixes is the key to expanding your vocabulary. Many English words are derived from Latin and Greek origins.', '理解词根和词缀是扩展词汇量的关键。许多英语单词源于拉丁语和希腊语来源。', NULL, NULL, 1, 600),
(1, '同义词辨析', 'Synonyms can have subtle differences in meaning and usage. For example, "big" and "large" are similar but used in different contexts.', '同义词在含义和用法上可能有细微差别。例如，"big" 和 "large" 相似但用于不同语境。', NULL, NULL, 2, 600),
(1, '真题例句', 'The government has implemented new policies to address environmental concerns.', '政府已实施新政策以解决环境问题。', NULL, NULL, 3, 600),
(2, '短对话训练', 'W: Could you tell me where the library is? M: Sure, go straight and turn left at the second crossing.', '女：你能告诉我图书馆在哪里吗？男：当然，直走在第二个路口左转。', NULL, NULL, 1, 600),
(2, '长对话训练', 'Today we will discuss the impact of social media on modern communication.', '今天我们将讨论社交媒体对现代交流的影响。', NULL, NULL, 2, 600),
(2, '讲座听力', 'Good morning everyone. In today lecture, we will explore the relationship between climate change and biodiversity loss.', '大家早上好。在今天的讲座中，我们将探讨气候变化与生物多样性丧失之间的关系。', NULL, NULL, 3, 600),
(3, '发音基础', 'Pronunciation is the foundation of spoken English. Pay attention to the difference between long and short vowel sounds.', '发音是英语口语的基础。注意长元音和短元音之间的区别。', NULL, NULL, 1, 600),
(3, '语调训练', 'Rising intonation is used for yes-no questions. Falling intonation is used for wh-questions and statements.', '升调用于一般疑问句，降调用于特殊疑问句和陈述句。', NULL, NULL, 2, 600),
(4, '大作文结构', 'A well-structured essay has three parts: introduction, body, and conclusion.', '结构良好的文章包括三部分：引言、正文和结论。', NULL, NULL, 1, 600),
(4, '高分句式', 'Using complex sentence structures can significantly improve your writing score.', '使用复杂句式可以显著提高你的写作分数。', NULL, NULL, 2, 600),
(5, '点餐场景', 'I would like to order a steak medium rare, please. Could I also have a glass of red wine?', '我想点一份五分熟的牛排。能再给我一杯红酒吗？', NULL, NULL, 1, 600),
(5, '问路场景', 'Excuse me, how do I get to the nearest subway station? Is it within walking distance?', '打扰一下，最近的地铁站怎么走？步行能到吗？', NULL, NULL, 2, 600);

INSERT INTO `membership_plans` (`name`, `price_cents`, `duration_days`, `description`, `features_json`, `is_active`) VALUES
('月度会员', 2900, 30, '基础学习功能，适合短期冲刺', '{"ai_dubbing": true, "srt_subtitle": true, "fsrs_review": true, "asmr_mix": true, "listening_mode": "basic", "download_limit": 50}', 1),
('季度会员', 6900, 90, '推荐选择，性价比最高', '{"ai_dubbing": true, "srt_subtitle": true, "fsrs_review": true, "asmr_mix": true, "listening_mode": "advanced", "download_limit": 200, "translation": "full"}', 1),
('年度会员', 19900, 365, '全年畅学，送专属学习规划', '{"ai_dubbing": true, "srt_subtitle": true, "fsrs_review": true, "asmr_mix": true, "listening_mode": "premium", "download_limit": -1, "translation": "full", "study_plan": true, "priority_support": true}', 1);

-- 给 student1 创建一个会员记录（已过期，用于测试续费）
INSERT INTO `user_memberships` (`user_id`, `plan_id`, `start_date`, `end_date`, `status`, `payment_method`, `transaction_id`) VALUES
(2, 1, DATE_SUB(NOW(), INTERVAL 60 DAY), DATE_SUB(NOW(), INTERVAL 30 DAY), 'expired', 'sandbox', 'sandbox_expired_001');
INSERT INTO `payments` (`user_id`, `amount_cents`, `payment_method`, `transaction_id`, `status`, `created_at`) VALUES
(2, 2900, 'sandbox', 'sandbox_expired_001', 'completed', DATE_SUB(NOW(), INTERVAL 60 DAY));