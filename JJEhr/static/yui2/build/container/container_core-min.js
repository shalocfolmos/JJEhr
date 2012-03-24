/*
 Copyright (c) 2011, Yahoo! Inc. All rights reserved.
 Code licensed under the BSD License:
 http://developer.yahoo.com/yui/license.html
 version: 2.9.0
 */
(function () {
    YAHOO.util.Config = function (d) {
        if (d) {
            this.init(d);
        }
    };
    var b = YAHOO.lang, c = YAHOO.util.CustomEvent, a = YAHOO.util.Config;
    a.CONFIG_CHANGED_EVENT = "configChanged";
    a.BOOLEAN_TYPE = "boolean";
    a.prototype = {owner:null, queueInProgress:false, config:null, initialConfig:null, eventQueue:null, configChangedEvent:null, init:function (d) {
        this.owner = d;
        this.configChangedEvent = this.createEvent(a.CONFIG_CHANGED_EVENT);
        this.configChangedEvent.signature = c.LIST;
        this.queueInProgress = false;
        this.config = {};
        this.initialConfig = {};
        this.eventQueue = [];
    }, checkBoolean:function (d) {
        return(typeof d == a.BOOLEAN_TYPE);
    }, checkNumber:function (d) {
        return(!isNaN(d));
    }, fireEvent:function (d, f) {
        var e = this.config[d];
        if (e && e.event) {
            e.event.fire(f);
        }
    }, addProperty:function (e, d) {
        e = e.toLowerCase();
        this.config[e] = d;
        d.event = this.createEvent(e, {scope:this.owner});
        d.event.signature = c.LIST;
        d.key = e;
        if (d.handler) {
            d.event.subscribe(d.handler, this.owner);
        }
        this.setProperty(e, d.value, true);
        if (!d.suppressEvent) {
            this.queueProperty(e, d.value);
        }
    }, getConfig:function () {
        var d = {}, f = this.config, g, e;
        for (g in f) {
            if (b.hasOwnProperty(f, g)) {
                e = f[g];
                if (e && e.event) {
                    d[g] = e.value;
                }
            }
        }
        return d;
    }, getProperty:function (d) {
        var e = this.config[d.toLowerCase()];
        if (e && e.event) {
            return e.value;
        } else {
            return undefined;
        }
    }, resetProperty:function (d) {
        d = d.toLowerCase();
        var e = this.config[d];
        if (e && e.event) {
            if (d in this.initialConfig) {
                this.setProperty(d, this.initialConfig[d]);
                return true;
            }
        } else {
            return false;
        }
    }, setProperty:function (e, g, d) {
        var f;
        e = e.toLowerCase();
        if (this.queueInProgress && !d) {
            this.queueProperty(e, g);
            return true;
        } else {
            f = this.config[e];
            if (f && f.event) {
                if (f.validator && !f.validator(g)) {
                    return false;
                } else {
                    f.value = g;
                    if (!d) {
                        this.fireEvent(e, g);
                        this.configChangedEvent.fire([e, g]);
                    }
                    return true;
                }
            } else {
                return false;
            }
        }
    }, queueProperty:function (v, r) {
        v = v.toLowerCase();
        var u = this.config[v], l = false, k, g, h, j, p, t, f, n, o, d, m, w, e;
        if (u && u.event) {
            if (!b.isUndefined(r) && u.validator && !u.validator(r)) {
                return false;
            } else {
                if (!b.isUndefined(r)) {
                    u.value = r;
                } else {
                    r = u.value;
                }
                l = false;
                k = this.eventQueue.length;
                for (m = 0; m < k; m++) {
                    g = this.eventQueue[m];
                    if (g) {
                        h = g[0];
                        j = g[1];
                        if (h == v) {
                            this.eventQueue[m] = null;
                            this.eventQueue.push([v, (!b.isUndefined(r) ? r : j)]);
                            l = true;
                            break;
                        }
                    }
                }
                if (!l && !b.isUndefined(r)) {
                    this.eventQueue.push([v, r]);
                }
            }
            if (u.supercedes) {
                p = u.supercedes.length;
                for (w = 0; w < p; w++) {
                    t = u.supercedes[w];
                    f = this.eventQueue.length;
                    for (e = 0; e < f; e++) {
                        n = this.eventQueue[e];
                        if (n) {
                            o = n[0];
                            d = n[1];
                            if (o == t.toLowerCase()) {
                                this.eventQueue.push([o, d]);
                                this.eventQueue[e] = null;
                                break;
                            }
                        }
                    }
                }
            }
            return true;
        } else {
            return false;
        }
    }, refireEvent:function (d) {
        d = d.toLowerCase();
        var e = this.config[d];
        if (e && e.event && !b.isUndefined(e.value)) {
            if (this.queueInProgress) {
                this.queueProperty(d);
            } else {
                this.fireEvent(d, e.value);
            }
        }
    }, applyConfig:function (d, g) {
        var f, e;
        if (g) {
            e = {};
            for (f in d) {
                if (b.hasOwnProperty(d, f)) {
                    e[f.toLowerCase()] = d[f];
                }
            }
            this.initialConfig = e;
        }
        for (f in d) {
            if (b.hasOwnProperty(d, f)) {
                this.queueProperty(f, d[f]);
            }
        }
    }, refresh:function () {
        var d;
        for (d in this.config) {
            if (b.hasOwnProperty(this.config, d)) {
                this.refireEvent(d);
            }
        }
    }, fireQueue:function () {
        var e, h, d, g, f;
        this.queueInProgress = true;
        for (e = 0; e < this.eventQueue.length; e++) {
            h = this.eventQueue[e];
            if (h) {
                d = h[0];
                g = h[1];
                f = this.config[d];
                f.value = g;
                this.eventQueue[e] = null;
                this.fireEvent(d, g);
            }
        }
        this.queueInProgress = false;
        this.eventQueue = [];
    }, subscribeToConfigEvent:function (d, e, g, h) {
        var f = this.config[d.toLowerCase()];
        if (f && f.event) {
            if (!a.alreadySubscribed(f.event, e, g)) {
                f.event.subscribe(e, g, h);
            }
            return true;
        } else {
            return false;
        }
    }, unsubscribeFromConfigEvent:function (d, e, g) {
        var f = this.config[d.toLowerCase()];
        if (f && f.event) {
            return f.event.unsubscribe(e, g);
        } else {
            return false;
        }
    }, toString:function () {
        var d = "Config";
        if (this.owner) {
            d += " [" + this.owner.toString() + "]";
        }
        return d;
    }, outputEventQueue:function () {
        var d = "", g, e, f = this.eventQueue.length;
        for (e = 0; e < f; e++) {
            g = this.eventQueue[e];
            if (g) {
                d += g[0] + "=" + g[1] + ", ";
            }
        }
        return d;
    }, destroy:function () {
        var e = this.config, d, f;
        for (d in e) {
            if (b.hasOwnProperty(e, d)) {
                f = e[d];
                f.event.unsubscribeAll();
                f.event = null;
            }
        }
        this.configChangedEvent.unsubscribeAll();
        this.configChangedEvent = null;
        this.owner = null;
        this.config = null;
        this.initialConfig = null;
        this.eventQueue = null;
    }};
    a.alreadySubscribed = function (e, h, j) {
        var f = e.subscribers.length, d, g;
        if (f > 0) {
            g = f - 1;
            do {
                d = e.subscribers[g];
                if (d && d.obj == j && d.fn == h) {
                    return true;
                }
            } while (g--);
        }
        return false;
    };
    YAHOO.lang.augmentProto(a, YAHOO.util.EventProvider);
}());
(function () {
    YAHOO.widget.Module = function (r, q) {
        if (r) {
            this.init(r, q);
        } else {
        }
    };
    var f = YAHOO.util.Dom, d = YAHOO.util.Config, n = YAHOO.util.Event, m = YAHOO.util.CustomEvent, g = YAHOO.widget.Module, i = YAHOO.env.ua, h, p, o, e, a = {"BEFORE_INIT":"beforeInit", "INIT":"init", "APPEND":"append", "BEFORE_RENDER":"beforeRender", "RENDER":"render", "CHANGE_HEADER":"changeHeader", "CHANGE_BODY":"changeBody", "CHANGE_FOOTER":"changeFooter", "CHANGE_CONTENT":"changeContent", "DESTROY":"destroy", "BEFORE_SHOW":"beforeShow", "SHOW":"show", "BEFORE_HIDE":"beforeHide", "HIDE":"hide"}, j = {"VISIBLE":{key:"visible", value:true, validator:YAHOO.lang.isBoolean}, "EFFECT":{key:"effect", suppressEvent:true, supercedes:["visible"]}, "MONITOR_RESIZE":{key:"monitorresize", value:true}, "APPEND_TO_DOCUMENT_BODY":{key:"appendtodocumentbody", value:false}};
    g.IMG_ROOT = null;
    g.IMG_ROOT_SSL = null;
    g.CSS_MODULE = "yui-module";
    g.CSS_HEADER = "hd";
    g.CSS_BODY = "bd";
    g.CSS_FOOTER = "ft";
    g.RESIZE_MONITOR_SECURE_URL = "javascript:false;";
    g.RESIZE_MONITOR_BUFFER = 1;
    g.textResizeEvent = new m("textResize");
    g.forceDocumentRedraw = function () {
        var q = document.documentElement;
        if (q) {
            q.className += " ";
            q.className = YAHOO.lang.trim(q.className);
        }
    };
    function l() {
        if (!h) {
            h = document.createElement("div");
            h.innerHTML = ('<div class="' + g.CSS_HEADER + '"></div>' + '<div class="' + g.CSS_BODY + '"></div><div class="' + g.CSS_FOOTER + '"></div>');
            p = h.firstChild;
            o = p.nextSibling;
            e = o.nextSibling;
        }
        return h;
    }

    function k() {
        if (!p) {
            l();
        }
        return(p.cloneNode(false));
    }

    function b() {
        if (!o) {
            l();
        }
        return(o.cloneNode(false));
    }

    function c() {
        if (!e) {
            l();
        }
        return(e.cloneNode(false));
    }

    g.prototype = {constructor:g, element:null, header:null, body:null, footer:null, id:null, imageRoot:g.IMG_ROOT, initEvents:function () {
        var q = m.LIST;
        this.beforeInitEvent = this.createEvent(a.BEFORE_INIT);
        this.beforeInitEvent.signature = q;
        this.initEvent = this.createEvent(a.INIT);
        this.initEvent.signature = q;
        this.appendEvent = this.createEvent(a.APPEND);
        this.appendEvent.signature = q;
        this.beforeRenderEvent = this.createEvent(a.BEFORE_RENDER);
        this.beforeRenderEvent.signature = q;
        this.renderEvent = this.createEvent(a.RENDER);
        this.renderEvent.signature = q;
        this.changeHeaderEvent = this.createEvent(a.CHANGE_HEADER);
        this.changeHeaderEvent.signature = q;
        this.changeBodyEvent = this.createEvent(a.CHANGE_BODY);
        this.changeBodyEvent.signature = q;
        this.changeFooterEvent = this.createEvent(a.CHANGE_FOOTER);
        this.changeFooterEvent.signature = q;
        this.changeContentEvent = this.createEvent(a.CHANGE_CONTENT);
        this.changeContentEvent.signature = q;
        this.destroyEvent = this.createEvent(a.DESTROY);
        this.destroyEvent.signature = q;
        this.beforeShowEvent = this.createEvent(a.BEFORE_SHOW);
        this.beforeShowEvent.signature = q;
        this.showEvent = this.createEvent(a.SHOW);
        this.showEvent.signature = q;
        this.beforeHideEvent = this.createEvent(a.BEFORE_HIDE);
        this.beforeHideEvent.signature = q;
        this.hideEvent = this.createEvent(a.HIDE);
        this.hideEvent.signature = q;
    }, platform:function () {
        var q = navigator.userAgent.toLowerCase();
        if (q.indexOf("windows") != -1 || q.indexOf("win32") != -1) {
            return"windows";
        } else {
            if (q.indexOf("macintosh") != -1) {
                return"mac";
            } else {
                return false;
            }
        }
    }(), browser:function () {
        var q = navigator.userAgent.toLowerCase();
        if (q.indexOf("opera") != -1) {
            return"opera";
        } else {
            if (q.indexOf("msie 7") != -1) {
                return"ie7";
            } else {
                if (q.indexOf("msie") != -1) {
                    return"ie";
                } else {
                    if (q.indexOf("safari") != -1) {
                        return"safari";
                    } else {
                        if (q.indexOf("gecko") != -1) {
                            return"gecko";
                        } else {
                            return false;
                        }
                    }
                }
            }
        }
    }(), isSecure:function () {
        if (window.location.href.toLowerCase().indexOf("https") === 0) {
            return true;
        } else {
            return false;
        }
    }(), initDefaultConfig:function () {
        this.cfg.addProperty(j.VISIBLE.key, {handler:this.configVisible, value:j.VISIBLE.value, validator:j.VISIBLE.validator});
        this.cfg.addProperty(j.EFFECT.key, {handler:this.configEffect, suppressEvent:j.EFFECT.suppressEvent, supercedes:j.EFFECT.supercedes});
        this.cfg.addProperty(j.MONITOR_RESIZE.key, {handler:this.configMonitorResize, value:j.MONITOR_RESIZE.value});
        this.cfg.addProperty(j.APPEND_TO_DOCUMENT_BODY.key, {value:j.APPEND_TO_DOCUMENT_BODY.value});
    }, init:function (v, u) {
        var s, w;
        this.initEvents();
        this.beforeInitEvent.fire(g);
        this.cfg = new d(this);
        if (this.isSecure) {
            this.imageRoot = g.IMG_ROOT_SSL;
        }
        if (typeof v == "string") {
            s = v;
            v = document.getElementById(v);
            if (!v) {
                v = (l()).cloneNode(false);
                v.id = s;
            }
        }
        this.id = f.generateId(v);
        this.element = v;
        w = this.element.firstChild;
        if (w) {
            var r = false, q = false, t = false;
            do {
                if (1 == w.nodeType) {
                    if (!r && f.hasClass(w, g.CSS_HEADER)) {
                        this.header = w;
                        r = true;
                    } else {
                        if (!q && f.hasClass(w, g.CSS_BODY)) {
                            this.body = w;
                            q = true;
                        } else {
                            if (!t && f.hasClass(w, g.CSS_FOOTER)) {
                                this.footer = w;
                                t = true;
                            }
                        }
                    }
                }
            } while ((w = w.nextSibling));
        }
        this.initDefaultConfig();
        f.addClass(this.element, g.CSS_MODULE);
        if (u) {
            this.cfg.applyConfig(u, true);
        }
        if (!d.alreadySubscribed(this.renderEvent, this.cfg.fireQueue, this.cfg)) {
            this.renderEvent.subscribe(this.cfg.fireQueue, this.cfg, true);
        }
        this.initEvent.fire(g);
    }, initResizeMonitor:function () {
        var r = (i.gecko && this.platform == "windows");
        if (r) {
            var q = this;
            setTimeout(function () {
                q._initResizeMonitor();
            }, 0);
        } else {
            this._initResizeMonitor();
        }
    }, _initResizeMonitor:function () {
        var q, s, u;

        function w() {
            g.textResizeEvent.fire();
        }

        if (!i.opera) {
            s = f.get("_yuiResizeMonitor");
            var v = this._supportsCWResize();
            if (!s) {
                s = document.createElement("iframe");
                if (this.isSecure && g.RESIZE_MONITOR_SECURE_URL && i.ie) {
                    s.src = g.RESIZE_MONITOR_SECURE_URL;
                }
                if (!v) {
                    u = ["<html><head><script ", 'type="text/javascript">', "window.onresize=function(){window.parent.", "YAHOO.widget.Module.textResizeEvent.", "fire();};<", "/script></head>", "<body></body></html>"].join("");
                    s.src = "data:text/html;charset=utf-8," + encodeURIComponent(u);
                }
                s.id = "_yuiResizeMonitor";
                s.title = "Text Resize Monitor";
                s.tabIndex = -1;
                s.setAttribute("role", "presentation");
                s.style.position = "absolute";
                s.style.visibility = "hidden";
                var r = document.body, t = r.firstChild;
                if (t) {
                    r.insertBefore(s, t);
                } else {
                    r.appendChild(s);
                }
                s.style.backgroundColor = "transparent";
                s.style.borderWidth = "0";
                s.style.width = "2em";
                s.style.height = "2em";
                s.style.left = "0";
                s.style.top = (-1 * (s.offsetHeight + g.RESIZE_MONITOR_BUFFER)) + "px";
                s.style.visibility = "visible";
                if (i.webkit) {
                    q = s.contentWindow.document;
                    q.open();
                    q.close();
                }
            }
            if (s && s.contentWindow) {
                g.textResizeEvent.subscribe(this.onDomResize, this, true);
                if (!g.textResizeInitialized) {
                    if (v) {
                        if (!n.on(s.contentWindow, "resize", w)) {
                            n.on(s, "resize", w);
                        }
                    }
                    g.textResizeInitialized = true;
                }
                this.resizeMonitor = s;
            }
        }
    }, _supportsCWResize:function () {
        var q = true;
        if (i.gecko && i.gecko <= 1.8) {
            q = false;
        }
        return q;
    }, onDomResize:function (s, r) {
        var q = -1 * (this.resizeMonitor.offsetHeight + g.RESIZE_MONITOR_BUFFER);
        this.resizeMonitor.style.top = q + "px";
        this.resizeMonitor.style.left = "0";
    }, setHeader:function (r) {
        var q = this.header || (this.header = k());
        if (r.nodeName) {
            q.innerHTML = "";
            q.appendChild(r);
        } else {
            q.innerHTML = r;
        }
        if (this._rendered) {
            this._renderHeader();
        }
        this.changeHeaderEvent.fire(r);
        this.changeContentEvent.fire();
    }, appendToHeader:function (r) {
        var q = this.header || (this.header = k());
        q.appendChild(r);
        this.changeHeaderEvent.fire(r);
        this.changeContentEvent.fire();
    }, setBody:function (r) {
        var q = this.body || (this.body = b());
        if (r.nodeName) {
            q.innerHTML = "";
            q.appendChild(r);
        } else {
            q.innerHTML = r;
        }
        if (this._rendered) {
            this._renderBody();
        }
        this.changeBodyEvent.fire(r);
        this.changeContentEvent.fire();
    }, appendToBody:function (r) {
        var q = this.body || (this.body = b());
        q.appendChild(r);
        this.changeBodyEvent.fire(r);
        this.changeContentEvent.fire();
    }, setFooter:function (r) {
        var q = this.footer || (this.footer = c());
        if (r.nodeName) {
            q.innerHTML = "";
            q.appendChild(r);
        } else {
            q.innerHTML = r;
        }
        if (this._rendered) {
            this._renderFooter();
        }
        this.changeFooterEvent.fire(r);
        this.changeContentEvent.fire();
    }, appendToFooter:function (r) {
        var q = this.footer || (this.footer = c());
        q.appendChild(r);
        this.changeFooterEvent.fire(r);
        this.changeContentEvent.fire();
    }, render:function (s, q) {
        var t = this;

        function r(u) {
            if (typeof u == "string") {
                u = document.getElementById(u);
            }
            if (u) {
                t._addToParent(u, t.element);
                t.appendEvent.fire();
            }
        }

        this.beforeRenderEvent.fire();
        if (!q) {
            q = this.element;
        }
        if (s) {
            r(s);
        } else {
            if (!f.inDocument(this.element)) {
                return false;
            }
        }
        this._renderHeader(q);
        this._renderBody(q);
        this._renderFooter(q);
        this._rendered = true;
        this.renderEvent.fire();
        return true;
    }, _renderHeader:function (q) {
        q = q || this.element;
        if (this.header && !f.inDocument(this.header)) {
            var r = q.firstChild;
            if (r) {
                q.insertBefore(this.header, r);
            } else {
                q.appendChild(this.header);
            }
        }
    }, _renderBody:function (q) {
        q = q || this.element;
        if (this.body && !f.inDocument(this.body)) {
            if (this.footer && f.isAncestor(q, this.footer)) {
                q.insertBefore(this.body, this.footer);
            } else {
                q.appendChild(this.body);
            }
        }
    }, _renderFooter:function (q) {
        q = q || this.element;
        if (this.footer && !f.inDocument(this.footer)) {
            q.appendChild(this.footer);
        }
    }, destroy:function (q) {
        var r, s = !(q);
        if (this.element) {
            n.purgeElement(this.element, s);
            r = this.element.parentNode;
        }
        if (r) {
            r.removeChild(this.element);
        }
        this.element = null;
        this.header = null;
        this.body = null;
        this.footer = null;
        g.textResizeEvent.unsubscribe(this.onDomResize, this);
        this.cfg.destroy();
        this.cfg = null;
        this.destroyEvent.fire();
    }, show:function () {
        this.cfg.setProperty("visible", true);
    }, hide:function () {
        this.cfg.setProperty("visible", false);
    }, configVisible:function (r, q, s) {
        var t = q[0];
        if (t) {
            if (this.beforeShowEvent.fire()) {
                f.setStyle(this.element, "display", "block");
                this.showEvent.fire();
            }
        } else {
            if (this.beforeHideEvent.fire()) {
                f.setStyle(this.element, "display", "none");
                this.hideEvent.fire();
            }
        }
    }, configEffect:function (r, q, s) {
        this._cachedEffects = (this.cacheEffects) ? this._createEffects(q[0]) : null;
    }, cacheEffects:true, _createEffects:function (t) {
        var q = null, u, r, s;
        if (t) {
            if (t instanceof Array) {
                q = [];
                u = t.length;
                for (r = 0; r < u; r++) {
                    s = t[r];
                    if (s.effect) {
                        q[q.length] = s.effect(this, s.duration);
                    }
                }
            } else {
                if (t.effect) {
                    q = [t.effect(this, t.duration)];
                }
            }
        }
        return q;
    }, configMonitorResize:function (s, r, t) {
        var q = r[0];
        if (q) {
            this.initResizeMonitor();
        } else {
            g.textResizeEvent.unsubscribe(this.onDomResize, this, true);
            this.resizeMonitor = null;
        }
    }, _addToParent:function (q, r) {
        if (!this.cfg.getProperty("appendtodocumentbody") && q === document.body && q.firstChild) {
            q.insertBefore(r, q.firstChild);
        } else {
            q.appendChild(r);
        }
    }, toString:function () {
        return"Module " + this.id;
    }};
    YAHOO.lang.augmentProto(g, YAHOO.util.EventProvider);
}());
(function () {
    YAHOO.widget.Overlay = function (p, o) {
        YAHOO.widget.Overlay.superclass.constructor.call(this, p, o);
    };
    var i = YAHOO.lang, m = YAHOO.util.CustomEvent, g = YAHOO.widget.Module, n = YAHOO.util.Event, f = YAHOO.util.Dom, d = YAHOO.util.Config, k = YAHOO.env.ua, b = YAHOO.widget.Overlay, h = "subscribe", e = "unsubscribe", c = "contained", j, a = {"BEFORE_MOVE":"beforeMove", "MOVE":"move"}, l = {"X":{key:"x", validator:i.isNumber, suppressEvent:true, supercedes:["iframe"]}, "Y":{key:"y", validator:i.isNumber, suppressEvent:true, supercedes:["iframe"]}, "XY":{key:"xy", suppressEvent:true, supercedes:["iframe"]}, "CONTEXT":{key:"context", suppressEvent:true, supercedes:["iframe"]}, "FIXED_CENTER":{key:"fixedcenter", value:false, supercedes:["iframe", "visible"]}, "WIDTH":{key:"width", suppressEvent:true, supercedes:["context", "fixedcenter", "iframe"]}, "HEIGHT":{key:"height", suppressEvent:true, supercedes:["context", "fixedcenter", "iframe"]}, "AUTO_FILL_HEIGHT":{key:"autofillheight", supercedes:["height"], value:"body"}, "ZINDEX":{key:"zindex", value:null}, "CONSTRAIN_TO_VIEWPORT":{key:"constraintoviewport", value:false, validator:i.isBoolean, supercedes:["iframe", "x", "y", "xy"]}, "IFRAME":{key:"iframe", value:(k.ie == 6 ? true : false), validator:i.isBoolean, supercedes:["zindex"]}, "PREVENT_CONTEXT_OVERLAP":{key:"preventcontextoverlap", value:false, validator:i.isBoolean, supercedes:["constraintoviewport"]}};
    b.IFRAME_SRC = "javascript:false;";
    b.IFRAME_OFFSET = 3;
    b.VIEWPORT_OFFSET = 10;
    b.TOP_LEFT = "tl";
    b.TOP_RIGHT = "tr";
    b.BOTTOM_LEFT = "bl";
    b.BOTTOM_RIGHT = "br";
    b.PREVENT_OVERLAP_X = {"tltr":true, "blbr":true, "brbl":true, "trtl":true};
    b.PREVENT_OVERLAP_Y = {"trbr":true, "tlbl":true, "bltl":true, "brtr":true};
    b.CSS_OVERLAY = "yui-overlay";
    b.CSS_HIDDEN = "yui-overlay-hidden";
    b.CSS_IFRAME = "yui-overlay-iframe";
    b.STD_MOD_RE = /^\s*?(body|footer|header)\s*?$/i;
    b.windowScrollEvent = new m("windowScroll");
    b.windowResizeEvent = new m("windowResize");
    b.windowScrollHandler = function (p) {
        var o = n.getTarget(p);
        if (!o || o === window || o === window.document) {
            if (k.ie) {
                if (!window.scrollEnd) {
                    window.scrollEnd = -1;
                }
                clearTimeout(window.scrollEnd);
                window.scrollEnd = setTimeout(function () {
                    b.windowScrollEvent.fire();
                }, 1);
            } else {
                b.windowScrollEvent.fire();
            }
        }
    };
    b.windowResizeHandler = function (o) {
        if (k.ie) {
            if (!window.resizeEnd) {
                window.resizeEnd = -1;
            }
            clearTimeout(window.resizeEnd);
            window.resizeEnd = setTimeout(function () {
                b.windowResizeEvent.fire();
            }, 100);
        } else {
            b.windowResizeEvent.fire();
        }
    };
    b._initialized = null;
    if (b._initialized === null) {
        n.on(window, "scroll", b.windowScrollHandler);
        n.on(window, "resize", b.windowResizeHandler);
        b._initialized = true;
    }
    b._TRIGGER_MAP = {"windowScroll":b.windowScrollEvent, "windowResize":b.windowResizeEvent, "textResize":g.textResizeEvent};
    YAHOO.extend(b, g, {CONTEXT_TRIGGERS:[], init:function (p, o) {
        b.superclass.init.call(this, p);
        this.beforeInitEvent.fire(b);
        f.addClass(this.element, b.CSS_OVERLAY);
        if (o) {
            this.cfg.applyConfig(o, true);
        }
        if (this.platform == "mac" && k.gecko) {
            if (!d.alreadySubscribed(this.showEvent, this.showMacGeckoScrollbars, this)) {
                this.showEvent.subscribe(this.showMacGeckoScrollbars, this, true);
            }
            if (!d.alreadySubscribed(this.hideEvent, this.hideMacGeckoScrollbars, this)) {
                this.hideEvent.subscribe(this.hideMacGeckoScrollbars, this, true);
            }
        }
        this.initEvent.fire(b);
    }, initEvents:function () {
        b.superclass.initEvents.call(this);
        var o = m.LIST;
        this.beforeMoveEvent = this.createEvent(a.BEFORE_MOVE);
        this.beforeMoveEvent.signature = o;
        this.moveEvent = this.createEvent(a.MOVE);
        this.moveEvent.signature = o;
    }, initDefaultConfig:function () {
        b.superclass.initDefaultConfig.call(this);
        var o = this.cfg;
        o.addProperty(l.X.key, {handler:this.configX, validator:l.X.validator, suppressEvent:l.X.suppressEvent, supercedes:l.X.supercedes});
        o.addProperty(l.Y.key, {handler:this.configY, validator:l.Y.validator, suppressEvent:l.Y.suppressEvent, supercedes:l.Y.supercedes});
        o.addProperty(l.XY.key, {handler:this.configXY, suppressEvent:l.XY.suppressEvent, supercedes:l.XY.supercedes});
        o.addProperty(l.CONTEXT.key, {handler:this.configContext, suppressEvent:l.CONTEXT.suppressEvent, supercedes:l.CONTEXT.supercedes});
        o.addProperty(l.FIXED_CENTER.key, {handler:this.configFixedCenter, value:l.FIXED_CENTER.value, validator:l.FIXED_CENTER.validator, supercedes:l.FIXED_CENTER.supercedes});
        o.addProperty(l.WIDTH.key, {handler:this.configWidth, suppressEvent:l.WIDTH.suppressEvent, supercedes:l.WIDTH.supercedes});
        o.addProperty(l.HEIGHT.key, {handler:this.configHeight, suppressEvent:l.HEIGHT.suppressEvent, supercedes:l.HEIGHT.supercedes});
        o.addProperty(l.AUTO_FILL_HEIGHT.key, {handler:this.configAutoFillHeight, value:l.AUTO_FILL_HEIGHT.value, validator:this._validateAutoFill, supercedes:l.AUTO_FILL_HEIGHT.supercedes});
        o.addProperty(l.ZINDEX.key, {handler:this.configzIndex, value:l.ZINDEX.value});
        o.addProperty(l.CONSTRAIN_TO_VIEWPORT.key, {handler:this.configConstrainToViewport, value:l.CONSTRAIN_TO_VIEWPORT.value, validator:l.CONSTRAIN_TO_VIEWPORT.validator, supercedes:l.CONSTRAIN_TO_VIEWPORT.supercedes});
        o.addProperty(l.IFRAME.key, {handler:this.configIframe, value:l.IFRAME.value, validator:l.IFRAME.validator, supercedes:l.IFRAME.supercedes});
        o.addProperty(l.PREVENT_CONTEXT_OVERLAP.key, {value:l.PREVENT_CONTEXT_OVERLAP.value, validator:l.PREVENT_CONTEXT_OVERLAP.validator, supercedes:l.PREVENT_CONTEXT_OVERLAP.supercedes});
    }, moveTo:function (o, p) {
        this.cfg.setProperty("xy", [o, p]);
    }, hideMacGeckoScrollbars:function () {
        f.replaceClass(this.element, "show-scrollbars", "hide-scrollbars");
    }, showMacGeckoScrollbars:function () {
        f.replaceClass(this.element, "hide-scrollbars", "show-scrollbars");
    }, _setDomVisibility:function (o) {
        f.setStyle(this.element, "visibility", (o) ? "visible" : "hidden");
        var p = b.CSS_HIDDEN;
        if (o) {
            f.removeClass(this.element, p);
        } else {
            f.addClass(this.element, p);
        }
    }, configVisible:function (x, w, t) {
        var p = w[0], B = f.getStyle(this.element, "visibility"), o = this._cachedEffects || this._createEffects(this.cfg.getProperty("effect")), A = (this.platform == "mac" && k.gecko), y = d.alreadySubscribed, q, v, s, r, u, z;
        if (B == "inherit") {
            v = this.element.parentNode;
            while (v.nodeType != 9 && v.nodeType != 11) {
                B = f.getStyle(v, "visibility");
                if (B != "inherit") {
                    break;
                }
                v = v.parentNode;
            }
            if (B == "inherit") {
                B = "visible";
            }
        }
        if (p) {
            if (A) {
                this.showMacGeckoScrollbars();
            }
            if (o) {
                if (p) {
                    if (B != "visible" || B === "" || this._fadingOut) {
                        if (this.beforeShowEvent.fire()) {
                            z = o.length;
                            for (s = 0; s < z; s++) {
                                q = o[s];
                                if (s === 0 && !y(q.animateInCompleteEvent, this.showEvent.fire, this.showEvent)) {
                                    q.animateInCompleteEvent.subscribe(this.showEvent.fire, this.showEvent, true);
                                }
                                q.animateIn();
                            }
                        }
                    }
                }
            } else {
                if (B != "visible" || B === "") {
                    if (this.beforeShowEvent.fire()) {
                        this._setDomVisibility(true);
                        this.cfg.refireEvent("iframe");
                        this.showEvent.fire();
                    }
                } else {
                    this._setDomVisibility(true);
                }
            }
        } else {
            if (A) {
                this.hideMacGeckoScrollbars();
            }
            if (o) {
                if (B == "visible" || this._fadingIn) {
                    if (this.beforeHideEvent.fire()) {
                        z = o.length;
                        for (r = 0; r < z; r++) {
                            u = o[r];
                            if (r === 0 && !y(u.animateOutCompleteEvent, this.hideEvent.fire, this.hideEvent)) {
                                u.animateOutCompleteEvent.subscribe(this.hideEvent.fire, this.hideEvent, true);
                            }
                            u.animateOut();
                        }
                    }
                } else {
                    if (B === "") {
                        this._setDomVisibility(false);
                    }
                }
            } else {
                if (B == "visible" || B === "") {
                    if (this.beforeHideEvent.fire()) {
                        this._setDomVisibility(false);
                        this.hideEvent.fire();
                    }
                } else {
                    this._setDomVisibility(false);
                }
            }
        }
    }, doCenterOnDOMEvent:function () {
        var o = this.cfg, p = o.getProperty("fixedcenter");
        if (o.getProperty("visible")) {
            if (p && (p !== c || this.fitsInViewport())) {
                this.center();
            }
        }
    }, fitsInViewport:function () {
        var s = b.VIEWPORT_OFFSET, q = this.element, t = q.offsetWidth, r = q.offsetHeight, o = f.getViewportWidth(), p = f.getViewportHeight();
        return((t + s < o) && (r + s < p));
    }, configFixedCenter:function (s, q, t) {
        var u = q[0], p = d.alreadySubscribed, r = b.windowResizeEvent, o = b.windowScrollEvent;
        if (u) {
            this.center();
            if (!p(this.beforeShowEvent, this.center)) {
                this.beforeShowEvent.subscribe(this.center);
            }
            if (!p(r, this.doCenterOnDOMEvent, this)) {
                r.subscribe(this.doCenterOnDOMEvent, this, true);
            }
            if (!p(o, this.doCenterOnDOMEvent, this)) {
                o.subscribe(this.doCenterOnDOMEvent, this, true);
            }
        } else {
            this.beforeShowEvent.unsubscribe(this.center);
            r.unsubscribe(this.doCenterOnDOMEvent, this);
            o.unsubscribe(this.doCenterOnDOMEvent, this);
        }
    }, configHeight:function (r, p, s) {
        var o = p[0], q = this.element;
        f.setStyle(q, "height", o);
        this.cfg.refireEvent("iframe");
    }, configAutoFillHeight:function (t, s, p) {
        var v = s[0], q = this.cfg, u = "autofillheight", w = "height", r = q.getProperty(u), o = this._autoFillOnHeightChange;
        q.unsubscribeFromConfigEvent(w, o);
        g.textResizeEvent.unsubscribe(o);
        this.changeContentEvent.unsubscribe(o);
        if (r && v !== r && this[r]) {
            f.setStyle(this[r], w, "");
        }
        if (v) {
            v = i.trim(v.toLowerCase());
            q.subscribeToConfigEvent(w, o, this[v], this);
            g.textResizeEvent.subscribe(o, this[v], this);
            this.changeContentEvent.subscribe(o, this[v], this);
            q.setProperty(u, v, true);
        }
    }, configWidth:function (r, o, s) {
        var q = o[0], p = this.element;
        f.setStyle(p, "width", q);
        this.cfg.refireEvent("iframe");
    }, configzIndex:function (q, o, r) {
        var s = o[0], p = this.element;
        if (!s) {
            s = f.getStyle(p, "zIndex");
            if (!s || isNaN(s)) {
                s = 0;
            }
        }
        if (this.iframe || this.cfg.getProperty("iframe") === true) {
            if (s <= 0) {
                s = 1;
            }
        }
        f.setStyle(p, "zIndex", s);
        this.cfg.setProperty("zIndex", s, true);
        if (this.iframe) {
            this.stackIframe();
        }
    }, configXY:function (q, p, r) {
        var t = p[0], o = t[0], s = t[1];
        this.cfg.setProperty("x", o);
        this.cfg.setProperty("y", s);
        this.beforeMoveEvent.fire([o, s]);
        o = this.cfg.getProperty("x");
        s = this.cfg.getProperty("y");
        this.cfg.refireEvent("iframe");
        this.moveEvent.fire([o, s]);
    }, configX:function (q, p, r) {
        var o = p[0], s = this.cfg.getProperty("y");
        this.cfg.setProperty("x", o, true);
        this.cfg.setProperty("y", s, true);
        this.beforeMoveEvent.fire([o, s]);
        o = this.cfg.getProperty("x");
        s = this.cfg.getProperty("y");
        f.setX(this.element, o, true);
        this.cfg.setProperty("xy", [o, s], true);
        this.cfg.refireEvent("iframe");
        this.moveEvent.fire([o, s]);
    }, configY:function (q, p, r) {
        var o = this.cfg.getProperty("x"), s = p[0];
        this.cfg.setProperty("x", o, true);
        this.cfg.setProperty("y", s, true);
        this.beforeMoveEvent.fire([o, s]);
        o = this.cfg.getProperty("x");
        s = this.cfg.getProperty("y");
        f.setY(this.element, s, true);
        this.cfg.setProperty("xy", [o, s], true);
        this.cfg.refireEvent("iframe");
        this.moveEvent.fire([o, s]);
    }, showIframe:function () {
        var p = this.iframe, o;
        if (p) {
            o = this.element.parentNode;
            if (o != p.parentNode) {
                this._addToParent(o, p);
            }
            p.style.display = "block";
        }
    }, hideIframe:function () {
        if (this.iframe) {
            this.iframe.style.display = "none";
        }
    }, syncIframe:function () {
        var o = this.iframe, q = this.element, s = b.IFRAME_OFFSET, p = (s * 2), r;
        if (o) {
            o.style.width = (q.offsetWidth + p + "px");
            o.style.height = (q.offsetHeight + p + "px");
            r = this.cfg.getProperty("xy");
            if (!i.isArray(r) || (isNaN(r[0]) || isNaN(r[1]))) {
                this.syncPosition();
                r = this.cfg.getProperty("xy");
            }
            f.setXY(o, [(r[0] - s), (r[1] - s)]);
        }
    }, stackIframe:function () {
        if (this.iframe) {
            var o = f.getStyle(this.element, "zIndex");
            if (!YAHOO.lang.isUndefined(o) && !isNaN(o)) {
                f.setStyle(this.iframe, "zIndex", (o - 1));
            }
        }
    }, configIframe:function (r, q, s) {
        var o = q[0];

        function t() {
            var v = this.iframe, w = this.element, x;
            if (!v) {
                if (!j) {
                    j = document.createElement("iframe");
                    if (this.isSecure) {
                        j.src = b.IFRAME_SRC;
                    }
                    if (k.ie) {
                        j.style.filter = "alpha(opacity=0)";
                        j.frameBorder = 0;
                    } else {
                        j.style.opacity = "0";
                    }
                    j.style.position = "absolute";
                    j.style.border = "none";
                    j.style.margin = "0";
                    j.style.padding = "0";
                    j.style.display = "none";
                    j.tabIndex = -1;
                    j.className = b.CSS_IFRAME;
                }
                v = j.cloneNode(false);
                v.id = this.id + "_f";
                x = w.parentNode;
                var u = x || document.body;
                this._addToParent(u, v);
                this.iframe = v;
            }
            this.showIframe();
            this.syncIframe();
            this.stackIframe();
            if (!this._hasIframeEventListeners) {
                this.showEvent.subscribe(this.showIframe);
                this.hideEvent.subscribe(this.hideIframe);
                this.changeContentEvent.subscribe(this.syncIframe);
                this._hasIframeEventListeners = true;
            }
        }

        function p() {
            t.call(this);
            this.beforeShowEvent.unsubscribe(p);
            this._iframeDeferred = false;
        }

        if (o) {
            if (this.cfg.getProperty("visible")) {
                t.call(this);
            } else {
                if (!this._iframeDeferred) {
                    this.beforeShowEvent.subscribe(p);
                    this._iframeDeferred = true;
                }
            }
        } else {
            this.hideIframe();
            if (this._hasIframeEventListeners) {
                this.showEvent.unsubscribe(this.showIframe);
                this.hideEvent.unsubscribe(this.hideIframe);
                this.changeContentEvent.unsubscribe(this.syncIframe);
                this._hasIframeEventListeners = false;
            }
        }
    }, _primeXYFromDOM:function () {
        if (YAHOO.lang.isUndefined(this.cfg.getProperty("xy"))) {
            this.syncPosition();
            this.cfg.refireEvent("xy");
            this.beforeShowEvent.unsubscribe(this._primeXYFromDOM);
        }
    }, configConstrainToViewport:function (p, o, q) {
        var r = o[0];
        if (r) {
            if (!d.alreadySubscribed(this.beforeMoveEvent, this.enforceConstraints, this)) {
                this.beforeMoveEvent.subscribe(this.enforceConstraints, this, true);
            }
            if (!d.alreadySubscribed(this.beforeShowEvent, this._primeXYFromDOM)) {
                this.beforeShowEvent.subscribe(this._primeXYFromDOM);
            }
        } else {
            this.beforeShowEvent.unsubscribe(this._primeXYFromDOM);
            this.beforeMoveEvent.unsubscribe(this.enforceConstraints, this);
        }
    }, configContext:function (u, t, q) {
        var x = t[0], r, o, v, s, p, w = this.CONTEXT_TRIGGERS;
        if (x) {
            r = x[0];
            o = x[1];
            v = x[2];
            s = x[3];
            p = x[4];
            if (w && w.length > 0) {
                s = (s || []).concat(w);
            }
            if (r) {
                if (typeof r == "string") {
                    this.cfg.setProperty("context", [document.getElementById(r), o, v, s, p], true);
                }
                if (o && v) {
                    this.align(o, v, p);
                }
                if (this._contextTriggers) {
                    this._processTriggers(this._contextTriggers, e, this._alignOnTrigger);
                }
                if (s) {
                    this._processTriggers(s, h, this._alignOnTrigger);
                    this._contextTriggers = s;
                }
            }
        }
    }, _alignOnTrigger:function (p, o) {
        this.align();
    }, _findTriggerCE:function (o) {
        var p = null;
        if (o instanceof m) {
            p = o;
        } else {
            if (b._TRIGGER_MAP[o]) {
                p = b._TRIGGER_MAP[o];
            }
        }
        return p;
    }, _processTriggers:function (s, v, r) {
        var q, u;
        for (var p = 0, o = s.length; p < o; ++p) {
            q = s[p];
            u = this._findTriggerCE(q);
            if (u) {
                u[v](r, this, true);
            } else {
                this[v](q, r);
            }
        }
    }, align:function (p, w, s) {
        var v = this.cfg.getProperty("context"), t = this, o, q, u;

        function r(z, A) {
            var y = null, x = null;
            switch (p) {
                case b.TOP_LEFT:
                    y = A;
                    x = z;
                    break;
                case b.TOP_RIGHT:
                    y = A - q.offsetWidth;
                    x = z;
                    break;
                case b.BOTTOM_LEFT:
                    y = A;
                    x = z - q.offsetHeight;
                    break;
                case b.BOTTOM_RIGHT:
                    y = A - q.offsetWidth;
                    x = z - q.offsetHeight;
                    break;
            }
            if (y !== null && x !== null) {
                if (s) {
                    y += s[0];
                    x += s[1];
                }
                t.moveTo(y, x);
            }
        }

        if (v) {
            o = v[0];
            q = this.element;
            t = this;
            if (!p) {
                p = v[1];
            }
            if (!w) {
                w = v[2];
            }
            if (!s && v[4]) {
                s = v[4];
            }
            if (q && o) {
                u = f.getRegion(o);
                switch (w) {
                    case b.TOP_LEFT:
                        r(u.top, u.left);
                        break;
                    case b.TOP_RIGHT:
                        r(u.top, u.right);
                        break;
                    case b.BOTTOM_LEFT:
                        r(u.bottom, u.left);
                        break;
                    case b.BOTTOM_RIGHT:
                        r(u.bottom, u.right);
                        break;
                }
            }
        }
    }, enforceConstraints:function (p, o, q) {
        var s = o[0];
        var r = this.getConstrainedXY(s[0], s[1]);
        this.cfg.setProperty("x", r[0], true);
        this.cfg.setProperty("y", r[1], true);
        this.cfg.setProperty("xy", r, true);
    }, _getConstrainedPos:function (y, p) {
        var t = this.element, r = b.VIEWPORT_OFFSET, A = (y == "x"), z = (A) ? t.offsetWidth : t.offsetHeight, s = (A) ? f.getViewportWidth() : f.getViewportHeight(), D = (A) ? f.getDocumentScrollLeft() : f.getDocumentScrollTop(), C = (A) ? b.PREVENT_OVERLAP_X : b.PREVENT_OVERLAP_Y, o = this.cfg.getProperty("context"), u = (z + r < s), w = this.cfg.getProperty("preventcontextoverlap") && o && C[(o[1] + o[2])], v = D + r, B = D + s - z - r, q = p;
        if (p < v || p > B) {
            if (w) {
                q = this._preventOverlap(y, o[0], z, s, D);
            } else {
                if (u) {
                    if (p < v) {
                        q = v;
                    } else {
                        if (p > B) {
                            q = B;
                        }
                    }
                } else {
                    q = v;
                }
            }
        }
        return q;
    }, _preventOverlap:function (y, w, z, u, C) {
        var A = (y == "x"), t = b.VIEWPORT_OFFSET, s = this, q = ((A) ? f.getX(w) : f.getY(w)) - C, o = (A) ? w.offsetWidth : w.offsetHeight, p = q - t, r = (u - (q + o)) - t, D = false, v = function () {
            var x;
            if ((s.cfg.getProperty(y) - C) > q) {
                x = (q - z);
            } else {
                x = (q + o);
            }
            s.cfg.setProperty(y, (x + C), true);
            return x;
        }, B = function () {
            var E = ((s.cfg.getProperty(y) - C) > q) ? r : p, x;
            if (z > E) {
                if (D) {
                    v();
                } else {
                    v();
                    D = true;
                    x = B();
                }
            }
            return x;
        };
        B();
        return this.cfg.getProperty(y);
    }, getConstrainedX:function (o) {
        return this._getConstrainedPos("x", o);
    }, getConstrainedY:function (o) {
        return this._getConstrainedPos("y", o);
    }, getConstrainedXY:function (o, p) {
        return[this.getConstrainedX(o), this.getConstrainedY(p)];
    }, center:function () {
        var r = b.VIEWPORT_OFFSET, s = this.element.offsetWidth, q = this.element.offsetHeight, p = f.getViewportWidth(), t = f.getViewportHeight(), o, u;
        if (s < p) {
            o = (p / 2) - (s / 2) + f.getDocumentScrollLeft();
        } else {
            o = r + f.getDocumentScrollLeft();
        }
        if (q < t) {
            u = (t / 2) - (q / 2) + f.getDocumentScrollTop();
        } else {
            u = r + f.getDocumentScrollTop();
        }
        this.cfg.setProperty("xy", [parseInt(o, 10), parseInt(u, 10)]);
        this.cfg.refireEvent("iframe");
        if (k.webkit) {
            this.forceContainerRedraw();
        }
    }, syncPosition:function () {
        var o = f.getXY(this.element);
        this.cfg.setProperty("x", o[0], true);
        this.cfg.setProperty("y", o[1], true);
        this.cfg.setProperty("xy", o, true);
    }, onDomResize:function (q, p) {
        var o = this;
        b.superclass.onDomResize.call(this, q, p);
        setTimeout(function () {
            o.syncPosition();
            o.cfg.refireEvent("iframe");
            o.cfg.refireEvent("context");
        }, 0);
    }, _getComputedHeight:(function () {
        if (document.defaultView && document.defaultView.getComputedStyle) {
            return function (p) {
                var o = null;
                if (p.ownerDocument && p.ownerDocument.defaultView) {
                    var q = p.ownerDocument.defaultView.getComputedStyle(p, "");
                    if (q) {
                        o = parseInt(q.height, 10);
                    }
                }
                return(i.isNumber(o)) ? o : null;
            };
        } else {
            return function (p) {
                var o = null;
                if (p.style.pixelHeight) {
                    o = p.style.pixelHeight;
                }
                return(i.isNumber(o)) ? o : null;
            };
        }
    })(), _validateAutoFillHeight:function (o) {
        return(!o) || (i.isString(o) && b.STD_MOD_RE.test(o));
    }, _autoFillOnHeightChange:function (r, p, q) {
        var o = this.cfg.getProperty("height");
        if ((o && o !== "auto") || (o === 0)) {
            this.fillHeight(q);
        }
    }, _getPreciseHeight:function (p) {
        var o = p.offsetHeight;
        if (p.getBoundingClientRect) {
            var q = p.getBoundingClientRect();
            o = q.bottom - q.top;
        }
        return o;
    }, fillHeight:function (r) {
        if (r) {
            var p = this.innerElement || this.element, o = [this.header, this.body, this.footer], v, w = 0, x = 0, t = 0, q = false;
            for (var u = 0, s = o.length; u < s; u++) {
                v = o[u];
                if (v) {
                    if (r !== v) {
                        x += this._getPreciseHeight(v);
                    } else {
                        q = true;
                    }
                }
            }
            if (q) {
                if (k.ie || k.opera) {
                    f.setStyle(r, "height", 0 + "px");
                }
                w = this._getComputedHeight(p);
                if (w === null) {
                    f.addClass(p, "yui-override-padding");
                    w = p.clientHeight;
                    f.removeClass(p, "yui-override-padding");
                }
                t = Math.max(w - x, 0);
                f.setStyle(r, "height", t + "px");
                if (r.offsetHeight != t) {
                    t = Math.max(t - (r.offsetHeight - t), 0);
                }
                f.setStyle(r, "height", t + "px");
            }
        }
    }, bringToTop:function () {
        var s = [], r = this.element;

        function v(z, y) {
            var B = f.getStyle(z, "zIndex"), A = f.getStyle(y, "zIndex"), x = (!B || isNaN(B)) ? 0 : parseInt(B, 10), w = (!A || isNaN(A)) ? 0 : parseInt(A, 10);
            if (x > w) {
                return -1;
            } else {
                if (x < w) {
                    return 1;
                } else {
                    return 0;
                }
            }
        }

        function q(y) {
            var x = f.hasClass(y, b.CSS_OVERLAY), w = YAHOO.widget.Panel;
            if (x && !f.isAncestor(r, y)) {
                if (w && f.hasClass(y, w.CSS_PANEL)) {
                    s[s.length] = y.parentNode;
                } else {
                    s[s.length] = y;
                }
            }
        }

        f.getElementsBy(q, "div", document.body);
        s.sort(v);
        var o = s[0], u;
        if (o) {
            u = f.getStyle(o, "zIndex");
            if (!isNaN(u)) {
                var t = false;
                if (o != r) {
                    t = true;
                } else {
                    if (s.length > 1) {
                        var p = f.getStyle(s[1], "zIndex");
                        if (!isNaN(p) && (u == p)) {
                            t = true;
                        }
                    }
                }
                if (t) {
                    this.cfg.setProperty("zindex", (parseInt(u, 10) + 2));
                }
            }
        }
    }, destroy:function (o) {
        if (this.iframe) {
            this.iframe.parentNode.removeChild(this.iframe);
        }
        this.iframe = null;
        b.windowResizeEvent.unsubscribe(this.doCenterOnDOMEvent, this);
        b.windowScrollEvent.unsubscribe(this.doCenterOnDOMEvent, this);
        g.textResizeEvent.unsubscribe(this._autoFillOnHeightChange);
        if (this._contextTriggers) {
            this._processTriggers(this._contextTriggers, e, this._alignOnTrigger);
        }
        b.superclass.destroy.call(this, o);
    }, forceContainerRedraw:function () {
        var o = this;
        f.addClass(o.element, "yui-force-redraw");
        setTimeout(function () {
            f.removeClass(o.element, "yui-force-redraw");
        }, 0);
    }, toString:function () {
        return"Overlay " + this.id;
    }});
}());
(function () {
    YAHOO.widget.OverlayManager = function (g) {
        this.init(g);
    };
    var d = YAHOO.widget.Overlay, c = YAHOO.util.Event, e = YAHOO.util.Dom, b = YAHOO.util.Config, f = YAHOO.util.CustomEvent, a = YAHOO.widget.OverlayManager;
    a.CSS_FOCUSED = "focused";
    a.prototype = {constructor:a, overlays:null, initDefaultConfig:function () {
        this.cfg.addProperty("overlays", {suppressEvent:true});
        this.cfg.addProperty("focusevent", {value:"mousedown"});
    }, init:function (i) {
        this.cfg = new b(this);
        this.initDefaultConfig();
        if (i) {
            this.cfg.applyConfig(i, true);
        }
        this.cfg.fireQueue();
        var h = null;
        this.getActive = function () {
            return h;
        };
        this.focus = function (j) {
            var k = this.find(j);
            if (k) {
                k.focus();
            }
        };
        this.remove = function (k) {
            var m = this.find(k), j;
            if (m) {
                if (h == m) {
                    h = null;
                }
                var l = (m.element === null && m.cfg === null) ? true : false;
                if (!l) {
                    j = e.getStyle(m.element, "zIndex");
                    m.cfg.setProperty("zIndex", -1000, true);
                }
                this.overlays.sort(this.compareZIndexDesc);
                this.overlays = this.overlays.slice(0, (this.overlays.length - 1));
                m.hideEvent.unsubscribe(m.blur);
                m.destroyEvent.unsubscribe(this._onOverlayDestroy, m);
                m.focusEvent.unsubscribe(this._onOverlayFocusHandler, m);
                m.blurEvent.unsubscribe(this._onOverlayBlurHandler, m);
                if (!l) {
                    c.removeListener(m.element, this.cfg.getProperty("focusevent"), this._onOverlayElementFocus);
                    m.cfg.setProperty("zIndex", j, true);
                    m.cfg.setProperty("manager", null);
                }
                if (m.focusEvent._managed) {
                    m.focusEvent = null;
                }
                if (m.blurEvent._managed) {
                    m.blurEvent = null;
                }
                if (m.focus._managed) {
                    m.focus = null;
                }
                if (m.blur._managed) {
                    m.blur = null;
                }
            }
        };
        this.blurAll = function () {
            var k = this.overlays.length, j;
            if (k > 0) {
                j = k - 1;
                do {
                    this.overlays[j].blur();
                } while (j--);
            }
        };
        this._manageBlur = function (j) {
            var k = false;
            if (h == j) {
                e.removeClass(h.element, a.CSS_FOCUSED);
                h = null;
                k = true;
            }
            return k;
        };
        this._manageFocus = function (j) {
            var k = false;
            if (h != j) {
                if (h) {
                    h.blur();
                }
                h = j;
                this.bringToTop(h);
                e.addClass(h.element, a.CSS_FOCUSED);
                k = true;
            }
            return k;
        };
        var g = this.cfg.getProperty("overlays");
        if (!this.overlays) {
            this.overlays = [];
        }
        if (g) {
            this.register(g);
            this.overlays.sort(this.compareZIndexDesc);
        }
    }, _onOverlayElementFocus:function (i) {
        var g = c.getTarget(i), h = this.close;
        if (h && (g == h || e.isAncestor(h, g))) {
            this.blur();
        } else {
            this.focus();
        }
    }, _onOverlayDestroy:function (h, g, i) {
        this.remove(i);
    }, _onOverlayFocusHandler:function (h, g, i) {
        this._manageFocus(i);
    }, _onOverlayBlurHandler:function (h, g, i) {
        this._manageBlur(i);
    }, _bindFocus:function (g) {
        var h = this;
        if (!g.focusEvent) {
            g.focusEvent = g.createEvent("focus");
            g.focusEvent.signature = f.LIST;
            g.focusEvent._managed = true;
        } else {
            g.focusEvent.subscribe(h._onOverlayFocusHandler, g, h);
        }
        if (!g.focus) {
            c.on(g.element, h.cfg.getProperty("focusevent"), h._onOverlayElementFocus, null, g);
            g.focus = function () {
                if (h._manageFocus(this)) {
                    if (this.cfg.getProperty("visible") && this.focusFirst) {
                        this.focusFirst();
                    }
                    this.focusEvent.fire();
                }
            };
            g.focus._managed = true;
        }
    }, _bindBlur:function (g) {
        var h = this;
        if (!g.blurEvent) {
            g.blurEvent = g.createEvent("blur");
            g.blurEvent.signature = f.LIST;
            g.focusEvent._managed = true;
        } else {
            g.blurEvent.subscribe(h._onOverlayBlurHandler, g, h);
        }
        if (!g.blur) {
            g.blur = function () {
                if (h._manageBlur(this)) {
                    this.blurEvent.fire();
                }
            };
            g.blur._managed = true;
        }
        g.hideEvent.subscribe(g.blur);
    }, _bindDestroy:function (g) {
        var h = this;
        g.destroyEvent.subscribe(h._onOverlayDestroy, g, h);
    }, _syncZIndex:function (g) {
        var h = e.getStyle(g.element, "zIndex");
        if (!isNaN(h)) {
            g.cfg.setProperty("zIndex", parseInt(h, 10));
        } else {
            g.cfg.setProperty("zIndex", 0);
        }
    }, register:function (g) {
        var k = false, h, j;
        if (g instanceof d) {
            g.cfg.addProperty("manager", {value:this});
            this._bindFocus(g);
            this._bindBlur(g);
            this._bindDestroy(g);
            this._syncZIndex(g);
            this.overlays.push(g);
            this.bringToTop(g);
            k = true;
        } else {
            if (g instanceof Array) {
                for (h = 0, j = g.length; h < j; h++) {
                    k = this.register(g[h]) || k;
                }
            }
        }
        return k;
    }, bringToTop:function (m) {
        var i = this.find(m), l, g, j;
        if (i) {
            j = this.overlays;
            j.sort(this.compareZIndexDesc);
            g = j[0];
            if (g) {
                l = e.getStyle(g.element, "zIndex");
                if (!isNaN(l)) {
                    var k = false;
                    if (g !== i) {
                        k = true;
                    } else {
                        if (j.length > 1) {
                            var h = e.getStyle(j[1].element, "zIndex");
                            if (!isNaN(h) && (l == h)) {
                                k = true;
                            }
                        }
                    }
                    if (k) {
                        i.cfg.setProperty("zindex", (parseInt(l, 10) + 2));
                    }
                }
                j.sort(this.compareZIndexDesc);
            }
        }
    }, find:function (g) {
        var l = g instanceof d, j = this.overlays, p = j.length, k = null, m, h;
        if (l || typeof g == "string") {
            for (h = p - 1; h >= 0; h--) {
                m = j[h];
                if ((l && (m === g)) || (m.id == g)) {
                    k = m;
                    break;
                }
            }
        }
        return k;
    }, compareZIndexDesc:function (j, i) {
        var h = (j.cfg) ? j.cfg.getProperty("zIndex") : null, g = (i.cfg) ? i.cfg.getProperty("zIndex") : null;
        if (h === null && g === null) {
            return 0;
        } else {
            if (h === null) {
                return 1;
            } else {
                if (g === null) {
                    return -1;
                } else {
                    if (h > g) {
                        return -1;
                    } else {
                        if (h < g) {
                            return 1;
                        } else {
                            return 0;
                        }
                    }
                }
            }
        }
    }, showAll:function () {
        var h = this.overlays, j = h.length, g;
        for (g = j - 1; g >= 0; g--) {
            h[g].show();
        }
    }, hideAll:function () {
        var h = this.overlays, j = h.length, g;
        for (g = j - 1; g >= 0; g--) {
            h[g].hide();
        }
    }, toString:function () {
        return"OverlayManager";
    }};
}());
(function () {
    YAHOO.widget.ContainerEffect = function (e, h, g, d, f) {
        if (!f) {
            f = YAHOO.util.Anim;
        }
        this.overlay = e;
        this.attrIn = h;
        this.attrOut = g;
        this.targetElement = d || e.element;
        this.animClass = f;
    };
    var b = YAHOO.util.Dom, c = YAHOO.util.CustomEvent, a = YAHOO.widget.ContainerEffect;
    a.FADE = function (d, f) {
        var g = YAHOO.util.Easing, i = {attributes:{opacity:{from:0, to:1}}, duration:f, method:g.easeIn}, e = {attributes:{opacity:{to:0}}, duration:f, method:g.easeOut}, h = new a(d, i, e, d.element);
        h.handleUnderlayStart = function () {
            var k = this.overlay.underlay;
            if (k && YAHOO.env.ua.ie) {
                var j = (k.filters && k.filters.length > 0);
                if (j) {
                    b.addClass(d.element, "yui-effect-fade");
                }
            }
        };
        h.handleUnderlayComplete = function () {
            var j = this.overlay.underlay;
            if (j && YAHOO.env.ua.ie) {
                b.removeClass(d.element, "yui-effect-fade");
            }
        };
        h.handleStartAnimateIn = function (k, j, l) {
            l.overlay._fadingIn = true;
            b.addClass(l.overlay.element, "hide-select");
            if (!l.overlay.underlay) {
                l.overlay.cfg.refireEvent("underlay");
            }
            l.handleUnderlayStart();
            l.overlay._setDomVisibility(true);
            b.setStyle(l.overlay.element, "opacity", 0);
        };
        h.handleCompleteAnimateIn = function (k, j, l) {
            l.overlay._fadingIn = false;
            b.removeClass(l.overlay.element, "hide-select");
            if (l.overlay.element.style.filter) {
                l.overlay.element.style.filter = null;
            }
            l.handleUnderlayComplete();
            l.overlay.cfg.refireEvent("iframe");
            l.animateInCompleteEvent.fire();
        };
        h.handleStartAnimateOut = function (k, j, l) {
            l.overlay._fadingOut = true;
            b.addClass(l.overlay.element, "hide-select");
            l.handleUnderlayStart();
        };
        h.handleCompleteAnimateOut = function (k, j, l) {
            l.overlay._fadingOut = false;
            b.removeClass(l.overlay.element, "hide-select");
            if (l.overlay.element.style.filter) {
                l.overlay.element.style.filter = null;
            }
            l.overlay._setDomVisibility(false);
            b.setStyle(l.overlay.element, "opacity", 1);
            l.handleUnderlayComplete();
            l.overlay.cfg.refireEvent("iframe");
            l.animateOutCompleteEvent.fire();
        };
        h.init();
        return h;
    };
    a.SLIDE = function (f, d) {
        var i = YAHOO.util.Easing, l = f.cfg.getProperty("x") || b.getX(f.element), k = f.cfg.getProperty("y") || b.getY(f.element), m = b.getClientWidth(), h = f.element.offsetWidth, j = {attributes:{points:{to:[l, k]}}, duration:d, method:i.easeIn}, e = {attributes:{points:{to:[(m + 25), k]}}, duration:d, method:i.easeOut}, g = new a(f, j, e, f.element, YAHOO.util.Motion);
        g.handleStartAnimateIn = function (o, n, p) {
            p.overlay.element.style.left = ((-25) - h) + "px";
            p.overlay.element.style.top = k + "px";
        };
        g.handleTweenAnimateIn = function (q, p, r) {
            var s = b.getXY(r.overlay.element), o = s[0], n = s[1];
            if (b.getStyle(r.overlay.element, "visibility") == "hidden" && o < l) {
                r.overlay._setDomVisibility(true);
            }
            r.overlay.cfg.setProperty("xy", [o, n], true);
            r.overlay.cfg.refireEvent("iframe");
        };
        g.handleCompleteAnimateIn = function (o, n, p) {
            p.overlay.cfg.setProperty("xy", [l, k], true);
            p.startX = l;
            p.startY = k;
            p.overlay.cfg.refireEvent("iframe");
            p.animateInCompleteEvent.fire();
        };
        g.handleStartAnimateOut = function (o, n, r) {
            var p = b.getViewportWidth(), s = b.getXY(r.overlay.element), q = s[1];
            r.animOut.attributes.points.to = [(p + 25), q];
        };
        g.handleTweenAnimateOut = function (p, o, q) {
            var s = b.getXY(q.overlay.element), n = s[0], r = s[1];
            q.overlay.cfg.setProperty("xy", [n, r], true);
            q.overlay.cfg.refireEvent("iframe");
        };
        g.handleCompleteAnimateOut = function (o, n, p) {
            p.overlay._setDomVisibility(false);
            p.overlay.cfg.setProperty("xy", [l, k]);
            p.animateOutCompleteEvent.fire();
        };
        g.init();
        return g;
    };
    a.prototype = {init:function () {
        this.beforeAnimateInEvent = this.createEvent("beforeAnimateIn");
        this.beforeAnimateInEvent.signature = c.LIST;
        this.beforeAnimateOutEvent = this.createEvent("beforeAnimateOut");
        this.beforeAnimateOutEvent.signature = c.LIST;
        this.animateInCompleteEvent = this.createEvent("animateInComplete");
        this.animateInCompleteEvent.signature = c.LIST;
        this.animateOutCompleteEvent = this.createEvent("animateOutComplete");
        this.animateOutCompleteEvent.signature = c.LIST;
        this.animIn = new this.animClass(this.targetElement, this.attrIn.attributes, this.attrIn.duration, this.attrIn.method);
        this.animIn.onStart.subscribe(this.handleStartAnimateIn, this);
        this.animIn.onTween.subscribe(this.handleTweenAnimateIn, this);
        this.animIn.onComplete.subscribe(this.handleCompleteAnimateIn, this);
        this.animOut = new this.animClass(this.targetElement, this.attrOut.attributes, this.attrOut.duration, this.attrOut.method);
        this.animOut.onStart.subscribe(this.handleStartAnimateOut, this);
        this.animOut.onTween.subscribe(this.handleTweenAnimateOut, this);
        this.animOut.onComplete.subscribe(this.handleCompleteAnimateOut, this);
    }, animateIn:function () {
        this._stopAnims(this.lastFrameOnStop);
        this.beforeAnimateInEvent.fire();
        this.animIn.animate();
    }, animateOut:function () {
        this._stopAnims(this.lastFrameOnStop);
        this.beforeAnimateOutEvent.fire();
        this.animOut.animate();
    }, lastFrameOnStop:true, _stopAnims:function (d) {
        if (this.animOut && this.animOut.isAnimated()) {
            this.animOut.stop(d);
        }
        if (this.animIn && this.animIn.isAnimated()) {
            this.animIn.stop(d);
        }
    }, handleStartAnimateIn:function (e, d, f) {
    }, handleTweenAnimateIn:function (e, d, f) {
    }, handleCompleteAnimateIn:function (e, d, f) {
    }, handleStartAnimateOut:function (e, d, f) {
    }, handleTweenAnimateOut:function (e, d, f) {
    }, handleCompleteAnimateOut:function (e, d, f) {
    }, toString:function () {
        var d = "ContainerEffect";
        if (this.overlay) {
            d += " [" + this.overlay.toString() + "]";
        }
        return d;
    }};
    YAHOO.lang.augmentProto(a, YAHOO.util.EventProvider);
})();
YAHOO.register("containercore", YAHOO.widget.Module, {version:"2.9.0", build:"2800"});