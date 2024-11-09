
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
def crawl_and_save_to_file(url, output_file):
    edge_options = Options()
    edge_options.add_argument("--headless")
    edge_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
    driver = webdriver.Edge(options=edge_options)
    driver.get(url)
    time.sleep(2)  
    try:
            response = requests.get(url, verify=False)
            if response.headers.get('Content-Type') == 'application/pdf':
                with open(output_file, 'wb') as pdf_file:
                    pdf_file.write(response.content)
                driver.quit()
                return
    except Exception as e:
            print(f"Có lỗi xảy ra khi tải xuống file PDF: {e}")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    wr_bottom = soup.find('div', id='wr_bottom')
    if wr_bottom:
        wr_bottom.decompose() 
    box_gray = soup.find('div', class_='box_gray bottom10 list-article-bottom')
    if box_gray:
        for p in box_gray.find_all('p'):
            p.decompose()  
    box_others = soup.find_all('div', class_='box_other pad10 clearfix')
    for box_other in box_others:
        box_other.clear() 
    modal_dialogs = soup.find_all('div', class_='modal-dialog')
    for modal_dialog in modal_dialogs:
        modal_dialog.clear()  
    popup_confirm_notify=soup.find('div',class_='popup-confirm-notify')
    if popup_confirm_notify:
        popup_confirm_notify.clear()
    binhluan = soup.find('div', class_='binhluan')
    if binhluan:
        binhluan.decompose() 
    other=soup.find('div',class_='other')
    if other:
        other.clear()
    AsideFirstZone_206=soup.find('div', id='AsideFirstZone_206')
    if AsideFirstZone_206:
        AsideFirstZone_206.clear()
    margin_5pxs=soup.find_all('div', style="margin:5px;border-top: 1px dashed #DDDDDD")
    for margin_5px in margin_5pxs :
        margin_5px.clear()
    col_md_7=soup.find('div',class_='col-md-7 col-sm-5')
    if col_md_7:
        col_md_7.clear()
    time_post=soup.find('p',class_='time-post text-change-size')
    if time_post:
        time_post.clear()
    portlet_title=soup.find('h1',class_='portlet-title')
    if portlet_title: 
        portlet_title.clear()
    titlebar_clearfixs=soup.find_all('div',class_='titlebar clearfix')
    for titlebar_clearfix in titlebar_clearfixs:
         titlebar_clearfix.clear()
    rows=soup.find_all('div',class_='col-xs-6 col-sm-4')
    for row in rows:
        row.clear()
    zonepage_r=soup.find('div',class_='zonepage-r')
    if zonepage_r:
        zonepage_r.clear()
    message_hidden=soup.find('div',class_='message hidden')
    if message_hidden:
        message_hidden.clear()
    commentform_clearfix=soup.find('div',class_='commentform clearfix')
    if commentform_clearfix:
        commentform_clearfix.clear()
    pnlCommentDialog=soup.find('div',id='pnlCommentDialog')
    if pnlCommentDialog:
        pnlCommentDialog.clear()
    storyothers_clearfix=soup.find('div',class_='storyothers clearfix')
    if storyothers_clearfix:
        storyothers_clearfix.clear()
    box_tinlienquan=soup.find('div',class_='content-right column')
    if box_tinlienquan:
        box_tinlienquan.clear()
    col_sm=soup.find('div',class_='col-sm-8 col-md-6')
    if col_sm:
        col_sm.clear()
    post_relate=soup.find('div',class_='post-relate')
    if post_relate:
        post_relate.clear()
    col_12=soup.find('div',class_='bg-white py-3 py-lg-4')
    if col_12:
        col_12.clear()
    item_news_other=soup.find('div',class_='item_news_other')
    if item_news_other:
        item_news_other.clear()
    panel_body_other=soup.find('div',class_='panel-body other-news')
    if panel_body_other:
        panel_body_other.clear()
    box_related_news=soup.find('div',class_='box-related-news')
    if box_related_news:
        box_related_news.clear()
    timeline_secondary=soup.find('div',class_='timeline secondary')
    if timeline_secondary:
        timeline_secondary.clear()
    note_btn=soup.find('div',class_='note-btn')
    if note_btn:
        note_btn.clear()
    panel_panel_default=soup.find('div',class_='col-xs-12 col-sm-12 col-md-12')
    if panel_panel_default:
        panel_panel_default.clear()
    relate_news=soup.find('div',class_='relate-news')
    if relate_news:
        relate_news.clear()
    section_maybelike=soup.find('section',class_='section-3 maybelike')
    if section_maybelike:
        section_maybelike.clear()
    section_3_d_none=soup.find('section',class_='section-3 d-none')
    if section_3_d_none:
        section_3_d_none.clear()
    section_1_section_3=soup.find('section',class_='section-1 section-3')
    if section_1_section_3:
        section_1_section_3.clear()
    box_tinkhac=soup.find('div',class_='box_tinkhac')
    if box_tinkhac :
        box_tinkhac.clear()
    more_news=soup.find('div',class_='tin-van')
    if more_news:
        more_news.clear()
    tab_content=soup.find('div',class_='tab-content')
    if tab_content:
        tab_content.clear()
    with open(output_file, 'w', encoding='utf-8') as file:
        headers = []
        for i in range(1, 2):
            headers.extend(soup.find_all(f'h{i}'))
        for header in headers:
            file.write(header.get_text(strip=True) + '\n')  
        footers = soup.find_all(lambda tag: tag.name == 'footer' or 
                                (tag.get('id') and 'footer' in tag.get('id')) or 
                                (tag.get('class') and any('footer' in cls for cls in tag.get('class'))))

        footer_elements = [footer for footer in footers]
        paragraphs = soup.find_all('p')
        for paragraph in paragraphs:
            if not any(paragraph in footer.find_all('p') for footer in footer_elements):
                file.write(paragraph.get_text(strip=True) + '\n') 
        body_text_div = soup.find('div', class_='bodytext margin-bottom-lg', id='news-bodyhtml')
        if body_text_div:
            file.write(body_text_div.get_text(strip=True) + '\n')
    with open(output_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    if len(lines) < 6:
        spans = soup.find_all('span')
        with open(output_file, 'a', encoding='utf-8') as file: 
            for span in spans:
                if not any(span in footer.find_all('span') for footer in footer_elements):
                    file.write(span.get_text(strip=True) + '\n')
    driver.quit()