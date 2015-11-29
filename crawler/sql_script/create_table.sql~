DROP TABLE IF EXISTS `test`.`published_url`;
CREATE TABLE  `test`.`published_url` (
  `url` varchar(512) CHARACTER SET latin1 COLLATE latin1_bin NOT NULL DEFAULT '',
  `create_time` int(10) unsigned zerofill NOT NULL DEFAULT '0000000000',
  `tag` varchar(255) CHARACTER SET latin1 NOT NULL DEFAULT '',
  `sub_tag` varchar(255) CHARACTER SET latin1 NOT NULL DEFAULT '',
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `version` varchar(45) NOT NULL,
  `count` int(10) unsigned NOT NULL DEFAULT '1',
  UNIQUE KEY `Index_url` (`url`) USING HASH,
  KEY `Index_time` (`create_time`) USING BTREE,
  KEY `Index_id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=ascii;
DROP TABLE IF EXISTS `test`.`successed_url`;
CREATE TABLE  `test`.`published_url` (
  `url` varchar(512) CHARACTER SET latin1 COLLATE latin1_bin NOT NULL DEFAULT '',
  `create_time` int(10) unsigned zerofill NOT NULL DEFAULT '0000000000',
  `tag` varchar(255) CHARACTER SET latin1 NOT NULL DEFAULT '',
  `sub_tag` varchar(255) CHARACTER SET latin1 NOT NULL DEFAULT '',
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `version` varchar(45) NOT NULL,
  `count` int(10) unsigned NOT NULL DEFAULT '1',
  UNIQUE KEY `Index_url` (`url`) USING HASH,
  KEY `Index_time` (`create_time`) USING BTREE,
  KEY `Index_id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=ascii;
DROP TABLE IF EXISTS `test`.`failed_url`;
CREATE TABLE  `test`.`published_url` (
  `url` varchar(512) CHARACTER SET latin1 COLLATE latin1_bin NOT NULL DEFAULT '',
  `create_time` int(10) unsigned zerofill NOT NULL DEFAULT '0000000000',
  `tag` varchar(255) CHARACTER SET latin1 NOT NULL DEFAULT '',
  `sub_tag` varchar(255) CHARACTER SET latin1 NOT NULL DEFAULT '',
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `version` varchar(45) NOT NULL,
  `count` int(10) unsigned NOT NULL DEFAULT '1',
  UNIQUE KEY `Index_url` (`url`) USING HASH,
  KEY `Index_time` (`create_time`) USING BTREE,
  KEY `Index_id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=ascii;
