DROP TABLE IF EXISTS `test`.`successed_url`;
CREATE TABLE  `test`.`successed_url` (
  `url` varchar(512) CHARACTER SET latin1 COLLATE latin1_bin NOT NULL,
  `create_time` bigint(20) unsigned NOT NULL DEFAULT '0',
  `tag` varchar(255) CHARACTER SET latin1 NOT NULL DEFAULT '',
  `sub_tag` varchar(255) CHARACTER SET latin1 NOT NULL DEFAULT '',
  `id` int(10) unsigned NOT NULL DEFAULT '0',
  `version` varchar(45) NOT NULL DEFAULT '',
  `count` int(10) unsigned NOT NULL DEFAULT '1',
  UNIQUE KEY `Index_url` (`url`) USING HASH,
  KEY `Index_time` (`create_time`) USING BTREE,
  KEY `Index_id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=ascii;
DROP TABLE IF EXISTS `test`.`failed_url`;
CREATE TABLE  `test`.`failed_url` (
  `url` varchar(512) CHARACTER SET latin1 COLLATE latin1_bin NOT NULL,
  `create_time` bigint(20) unsigned NOT NULL DEFAULT '0',
  `tag` varchar(255) CHARACTER SET latin1 NOT NULL DEFAULT '',
  `sub_tag` varchar(255) CHARACTER SET latin1 NOT NULL DEFAULT '',
  `id` int(10) unsigned NOT NULL DEFAULT '0',
  `version` varchar(45) NOT NULL DEFAULT '',
  `count` int(10) unsigned NOT NULL DEFAULT '1',
  UNIQUE KEY `Index_url` (`url`) USING HASH,
  KEY `Index_time` (`create_time`) USING BTREE,
  KEY `Index_id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=ascii;
DROP TABLE IF EXISTS `test`.`published_url`;
CREATE TABLE  `test`.`published_url` (
  `url` varchar(512) CHARACTER SET latin1 COLLATE latin1_bin NOT NULL,
  `create_time` bigint(20) unsigned NOT NULL DEFAULT '0',
  `tag` varchar(255) CHARACTER SET latin1 NOT NULL DEFAULT '',
  `sub_tag` varchar(255) CHARACTER SET latin1 NOT NULL DEFAULT '',
  `id` int(10) unsigned NOT NULL DEFAULT '0',
  `version` varchar(45) NOT NULL DEFAULT '',
  `count` int(10) unsigned NOT NULL DEFAULT '1',
  UNIQUE KEY `Index_url` (`url`) USING HASH,
  KEY `Index_time` (`create_time`) USING BTREE,
  KEY `Index_id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=ascii;
