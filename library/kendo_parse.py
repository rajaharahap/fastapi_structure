class KendoParse(object):

    def parse_query(self, orderby, limit, offset, filter, filter_other="", filter_other_conj=""):
        str_clause = " {where} {orderby} {limit} {offset}"
        return str(str_clause).replace('{orderby}', self.__generate_orderby(orderby)).\
                           replace('{limit}', self.__generate_limit(limit)).\
                           replace('{offset}', self.__generate_offset(offset)).\
                           replace('{where}', self.__generate_filter(filter, filter_other, filter_other_conj))

    def __generate_filter(self, filter, filter_other, filter_other_conj):
        if filter is None:
            if filter_other == '':
                filter_parse = ""
            else:
                filter_parse = f"where {filter_other}"
        elif ' and ' in filter and 'or' in filter:
            filter_parse = f"where {self.__render_filter(' and ', ' or ', filter)} {filter_other_conj} {filter_other}"
        elif ' and ' in filter:
            filter_parse = f"where {self.__render_filter(' and ','', filter)} {filter_other_conj} {filter_other}"
        elif ' or ' in filter:
            filter_parse = f"where {self.__render_filter(' or ','', filter)} {filter_other_conj} {filter_other}"
        else:
            filter_parse = f"where {self.__render_filter('','', filter)} {filter_other_conj} {filter_other}"
        return filter_parse

    def __generate_orderby(self, orderby):
        if orderby is None or orderby == "":
            orderby_parse = ""
        else:
            orderby_parse = f" ORDER BY {orderby}"
        return orderby_parse

    def __generate_limit(self, limit):
        if limit is None:
            limit_parse = ""
        else:
            limit_parse = f" LIMIT {limit}"
        return limit_parse

    def __generate_offset(self, offset):
        if offset is None:
            offset_parse = ""
        else:
            offset_parse = f" OFFSET {offset}"
        return offset_parse

    def __render_filter(self, conj, conj2, string):
        newString = str(string)
        newReturnString = ''
        if conj != '':
            if conj2 != '':
                newString.replace(conj2, conj)
            newStringSplit = newString[1:(len(newString) - 1)].split(conj)
            count = len(newStringSplit)
            i = 0
            while i < count:
                if i == 0:
                    newReturnString = self.__string_conj(str(newStringSplit[i]))
                else:
                    newReturnString = f"{newReturnString} {conj} {self.__string_conj(str(newStringSplit[i]))}"
                i+=1
        else:
            newReturnString = self.__string_conj(string)
        return newReturnString

    def __string_conj(self, string):
        if 'contains' in string:
            return self.__filter_contains(string)
        elif ' eq -1' in string:
            return self.__filter_not_contains(string)
        elif ' eq null' in string:
            return self.__filter_isnull(string)
        elif ' ne null' in string:
            return self.__filter_isnotnull(string)
        elif " eq ''" in string:
            return self.__filter_isempty(string)
        elif " ne ''" in string:
            return self.__filter_isnotempty(string)
        elif ' eq ' in string:
            return self.__filter_equal(string)
        elif ' ne ' in string:
            return self.__filter_not_equal(string)
        elif 'startswith' in string:
            return self.__filter_startswith(string)
        elif 'endswith' in string:
            return self.__filter_endswith(string)

    def __filter_contains(self, string):
        newString = str(string).lower(). \
            replace('contains(', ''). \
            replace(')', ''). \
            replace('(', ''). \
            replace("'", ''). \
            replace(" or ", ','). \
            split(',')
        count = len(newString)
        i = 0
        newReturnString = ''
        while i < count:
            #This would return ERROR in Postgresql since text() is not a function
            # newReturnString += f"""lower(text("{newString[i]}")) like '%%{newString[i+1]}%%'"""
            newReturnString += f"""lower(({newString[i]})) like '%%{newString[i+1]}%%'"""
            if i != count - 2:
                newReturnString += f" or "
            i += 2
        return f"( " + newReturnString + f" )"

    def __filter_not_contains(self, string):
        newString = str(string).lower(). \
            replace('indexof(', ''). \
            replace(') eq -1', ''). \
            replace("'", ''). \
            split(',')
        return f" lower(text({newString[0]})) not like '%%{newString[1]}%%'"

    def __filter_equal(self, string):
        newString = str(string).lower().replace(' eq ', ' = ')
        return newString

    def __filter_not_equal(self, string):
        newString = str(string).lower().replace(' ne ', ' != ')
        return newString

    def __filter_startswith(self, string):
        newString = str(string).lower(). \
            replace('startswith(', ''). \
            replace(')', ''). \
            replace("'", ''). \
            split(',')
        return f" lower(text({newString[0]})) like '{newString[1]}%%'"

    def __filter_endswith(self, string):
        newString = str(string).lower(). \
            replace('endswith(', ''). \
            replace(')', ''). \
            replace("'", ''). \
            split(',')
        return f" lower(text({newString[0]})) like '%%{newString[1]}'"

    def __filter_isnull(self, string):
        newString = str(string).lower().replace(' eq ', ' is ')
        return newString

    def __filter_isnotnull(self, string):
        newString = str(string).lower().replace(' ne ', ' is not ')
        return newString

    def __filter_isempty(self, string):
        newString = str(string).lower().replace(' eq ', ' = ')
        return newString

    def __filter_isnotempty(self, string):
        newString = str(string).lower().replace(' ne ', ' != ')
        return newString
