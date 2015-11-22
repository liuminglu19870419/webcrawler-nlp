DROP TABLE IF EXISTS `test`.`published_url`;
CREATE TABLE  `test`.`published_url` (
  `url` varchar(512) CHARACTER SET latin1 COLLATE latin1_bin NOT NULL DEFAULT '',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `tag` varchar(255) CHARACTER SET latin1 NOT NULL DEFAULT '',
  `sub_tag` varchar(255) CHARACTER SET latin1 NOT NULL DEFAULT '',
  `id` int(10) unsigned NOT NULL DEFAULT '0',
  UNIQUE KEY `Index_url` (`url`) USING HASH
) ENGINE=MyISAM DEFAULT CHARSET=ascii;
